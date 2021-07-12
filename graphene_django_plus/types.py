import datetime
import decimal
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, Union

from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db import models
from django.db.models import Prefetch
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel
import graphene
from graphene.utils.str_converters import to_camel_case
from graphene_django import DjangoObjectType
from graphene_django.converter import get_choices
from graphene_django.types import DjangoObjectTypeOptions

try:
    import graphene_django_optimizer as gql_optimizer

    _BaseDjangoObjectType = gql_optimizer.OptimizedDjangoObjectType
except ImportError:
    gql_optimizer = None
    _BaseDjangoObjectType = DjangoObjectType

from .models import GuardedModel, GuardedModelManager
from .perms import check_authenticated, check_perms
from .schema import FieldKind, get_field_schema
from .utils import get_model_fields, update_dict_nested

if TYPE_CHECKING:
    _BaseDjangoObjectType = DjangoObjectType

_T = TypeVar("_T", bound=models.Model)
schema_registry = {}


def schema_for_field(field, name):
    s = get_field_schema(field)

    default_value = getattr(field, "default", None)
    if default_value is NOT_PROVIDED:
        default_value = None
    if default_value is not None and callable(default_value):
        default_value = default_value()
    if default_value is not None:
        if isinstance(default_value, decimal.Decimal):
            default_value = str(default_value)
        if isinstance(default_value, (datetime.datetime, datetime.date, datetime.time)):
            default_value = default_value.isoformat()

    if isinstance(field, (ManyToOneRel, ManyToManyRel)):
        required = not field.null
    else:
        required = not field.blank and field.default is NOT_PROVIDED

    if getattr(field, "choices", None):
        items = field.choices
        if isinstance(items, dict):
            items = items.items()

        choices = []
        for (_original_v, label), (n, _value, _desc) in zip(items, get_choices(items)):
            choices.append(
                {
                    "label": label,
                    "value": n,
                }
            )
    else:
        choices = None

    s = update_dict_nested(
        s,
        {
            "name": to_camel_case(name),
            # FIXME: Get verbose_name and help_text for m2m
            "label": getattr(field, "verbose_name", None),
            "help_text": getattr(field, "help_text", None),
            "hidden": name == "id",
            "choices": choices,
            "default_value": default_value,
            "validation": {
                "required": required,
                "min_length": getattr(field, "min_length", None),
                "max_length": getattr(field, "max_length", None),
                "min_value": None,
                "max_value": None,
            },
        },
    )

    return s


class MutationErrorType(graphene.ObjectType):
    """An error that happened in a mutation."""

    field = graphene.String(
        description=(
            "The field that caused the error, or `null` if it "
            "isn't associated with any particular field."
        ),
        required=False,
    )
    message = graphene.String(
        description="The error message.",
    )


class InputSchemaFieldChoiceType(graphene.ObjectType):
    """An input schema field choice."""

    label = graphene.String(
        description="The choice's label.",
        required=True,
    )
    value = graphene.String(
        description="The choice's value.",
        required=True,
    )


class SchemaFieldValidationType(graphene.ObjectType):
    """Validation data for the field."""

    required = graphene.Boolean(
        description="If this field is required.",
        required=True,
        default_value=False,
    )
    min_value = graphene.JSONString(
        description="Min value for the field. Parse the json to get its value.",
        required=False,
        default_value=None,
    )
    max_value = graphene.JSONString(
        description="Max value for the field. Parse the json to get its value.",
        required=False,
        default_value=None,
    )
    min_length = graphene.Int(
        description="Min length for string kinds.",
        required=False,
        default_value=None,
    )
    max_length = graphene.Int(
        description="Max length for string kinds.",
        required=False,
        default_value=None,
    )
    max_digits = graphene.Int(
        description="Max digits for decimal kinds (null otherwise).",
        required=False,
        default_value=None,
    )
    decimal_places = graphene.Int(
        description="Max digits for decimal kinds (null otherwise).",
        required=False,
        default_value=None,
    )


class SchemaFieldType(graphene.ObjectType):
    """The input schema field."""

    name = graphene.String(
        description="The name of the field",
        required=True,
    )
    kind = FieldKind(
        description="The kind of this field.",
        required=True,
    )
    of_type = graphene.String(
        description="The name of the related field for ID kinds.",
        required=False,
        default_value=None,
    )
    multiple = graphene.Boolean(
        description="If this field expects an array of values.",
        required=True,
        default_value=False,
    )
    choices = graphene.List(
        graphene.NonNull(InputSchemaFieldChoiceType),
        description="Choices for this field.",
        required=False,
        default_value=None,
    )
    hidden = graphene.Boolean(
        description="If this field should be displayed in a hidden field.",
        required=True,
        default_value=False,
    )
    label = graphene.String(
        description="The field's humanized name.",
        required=False,
        default_value=None,
    )
    help_text = graphene.String(
        description="A help text for the field.",
        required=False,
        default_value=None,
    )
    default_value = graphene.JSONString(
        description="Default value for the field. Parse the json to get its value.",
        required=False,
        default_value=None,
    )
    validation = graphene.Field(
        SchemaFieldValidationType,
        description="Validation metadata for this field.",
        required=True,
    )


class SchemaType(graphene.ObjectType):
    """The input schema."""

    object_type = graphene.String(
        description="The name of the input object.",
        required=True,
    )
    fields = graphene.List(
        graphene.NonNull(SchemaFieldType),
        description="The fields in the input object.",
        required=True,
    )


class UploadType(graphene.types.Scalar):
    """The upload of a file.

    Variables of this type must be set to null in mutations. They will be
    replaced with a filename from a following multipart part containing a
    binary file.

    See: https://github.com/jaydenseric/graphql-multipart-request-spec
    """

    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


class ModelTypeOptions(DjangoObjectTypeOptions):
    """Model type options for :class:`ModelType`."""

    #: If we shuld allow unauthenticated users to query for this model.
    allow_unauthenticated: bool = False

    #: A list of django permissions to check if the user has permission to
    #: query this model.
    permissions: Optional[List[str]] = None

    #: If any permission should allow the user to query this model.
    permissions_any: bool = True

    #: A list of guardian object permissions to check if the user has
    #: permission to query the model object.
    object_permissions: Optional[List[str]] = None

    #: If any object permission should allow the user to query this model.
    object_permissions_any: bool = True

    #: The fields schema for the schema query
    fields_schema: Optional[dict] = None


class ModelType(_BaseDjangoObjectType, Generic[_T]):
    """Base type with automatic optimizations and permissions checking."""

    class Meta:
        abstract = True

    @classmethod
    def __class_getitem__(cls, *args, **kwargs):
        return cls

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        _meta=None,
        model=None,
        permissions=None,
        permissions_any=True,
        object_permissions=None,
        object_permissions_any=True,
        fields_schema=None,
        allow_unauthenticated=False,
        only_fields=None,
        fields=None,
        exclude_fields=None,
        exclude=None,
        **kwargs,
    ):
        if not _meta:
            _meta = ModelTypeOptions(cls)

        _meta.permissions = permissions or []
        _meta.permissions_any = permissions_any
        _meta.object_permissions = object_permissions or []
        _meta.object_permissions_any = object_permissions_any
        _meta.allow_unauthenticated = allow_unauthenticated

        _fields_schema = {}
        # graphene will handle the deprecated only_fields/exclude_fields for us
        # We just want to mimic the logic here
        _include = fields if fields is not None else only_fields
        if _include is not None:
            _include = set(_include)
        _exclude = set(exclude or []) or set(exclude_fields or [])
        for name, field in get_model_fields(model):
            if name in _exclude:
                continue
            if _include is not None and name not in _include:
                continue

            _fields_schema[name] = schema_for_field(field, name)

        fields_schema = update_dict_nested(
            _fields_schema,
            fields_schema or {},
        )
        _meta.fields_schema = fields_schema or {}

        super().__init_subclass_with_meta__(
            _meta=_meta,
            model=model,
            only_fields=only_fields,
            fields=fields,
            exclude_fields=exclude_fields,
            exclude=exclude,
            **kwargs,
        )

        schema_registry[cls._meta.name] = {
            "object_type": cls._meta.name,
            "fields": list(_meta.fields_schema.values()),
        }

    @classmethod
    def get_queryset(
        cls,
        qs: Union[models.QuerySet[_T], models.Manager[_T]],
        info,
    ) -> models.QuerySet[_T]:
        """Get the queryset checking for permissions and optimizing the query.

        Override the default graphene's `get_queryset` to check for permissions
        and optimize the query performance.

        Note that the query will only be automaticallu optimized if,
        `graphene_django_optimizer` is installed.
        """
        if isinstance(qs, models.Manager):
            qs = qs.get_queryset()

        if not cls.check_permissions(info.context.user):
            return qs.none()

        if cls._meta.object_permissions and isinstance(
            cls._meta.model.objects, GuardedModelManager
        ):
            qs &= cls._meta.model.objects.for_user(
                info.context.user,
                cls._meta.object_permissions,
                any_perm=cls._meta.object_permissions_any,
            )

        ret = super().get_queryset(qs, info)
        if gql_optimizer is None:
            return ret

        ret = gql_optimizer.query(ret, info)
        prl = {
            i.to_attr if isinstance(i, Prefetch) else i: i for i in ret._prefetch_related_lookups
        }
        ret._prefetch_related_lookups = tuple(prl.values())

        return ret

    @classmethod
    def get_node(cls, info, id_) -> Optional[_T]:
        """Get the node instance given the relay global id."""
        # NOTE: get_queryset will filter allowed models for the user so
        # this will return None if he is not allowed to retrieve this

        if gql_optimizer is not None:
            # optimizer will ignore queryset so call the same as they call
            # but passing objects from get_queryset to keep our preferences
            try:
                instance = cls.get_queryset(cls._meta.model.objects, info).get(
                    pk=id_,
                )
            except cls._meta.model.DoesNotExist:
                instance = None
        else:
            instance = super().get_node(info, id_)

        if instance is not None and not cls.check_object_permissions(info.context.user, instance):
            return None

        return instance

    @classmethod
    def check_permissions(cls, user: Union[AbstractUser, AnonymousUser]) -> bool:
        """Check permissions for the given user.

        Subclasses can override this to avoid the permission checking or
        extending it. Remember to call `super()` in the later case.
        """
        if not cls._meta.allow_unauthenticated and not check_authenticated(user):
            return False

        if not cls._meta.permissions:
            return True

        return check_perms(user, cls._meta.permissions, any_perm=cls._meta.permissions_any)

    @classmethod
    def check_object_permissions(
        cls,
        user: Union[AbstractUser, AnonymousUser],
        instance: _T,
    ) -> bool:
        """Check object permissions for the given user.

        Subclasses can override this to avoid the permission checking or
        extending it. Remember to call `super()` in the later case.

        For this to work, the model needs to implement a `has_perm` method.
        The easiest way when using `guardian` is to inherit it
        from :class:`graphene_django_plus.models.GuardedModel`.
        """
        if not cls._meta.object_permissions:
            return True

        if not isinstance(instance, GuardedModel):
            return True

        return instance.has_perm(
            user,
            cls._meta.object_permissions,
            any_perm=cls._meta.object_permissions_any,
        )
