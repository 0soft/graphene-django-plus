# This was based on some code from https://github.com/mirumee/saleor
# but adapted to use relay, automatic field detection and some code adjustments

import collections
import collections.abc
import itertools
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.core.exceptions import NON_FIELD_ERRORS, ImproperlyConfigured
from django.core.exceptions import PermissionDenied as DJPermissionDenied
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel
import graphene
from graphene.relay.mutation import ClientIDMutation
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene.utils.str_converters import to_camel_case
from graphene_django.converter import convert_django_field_with_choices
from graphene_django.registry import get_global_registry
from graphql.error import GraphQLError

from .exceptions import PermissionDenied
from .models import GuardedModel
from .perms import check_authenticated, check_perms
from .settings import graphene_django_plus_settings
from .types import MutationErrorType, UploadType, schema_for_field, schema_registry
from .utils import get_model_fields, get_node, get_nodes, update_dict_nested

_registry = get_global_registry()
_T = TypeVar("_T", bound=models.Model)
_M = TypeVar("_M", bound="BaseMutation")
_MM = TypeVar("_MM", bound="ModelMutation")


def _get_model_name(model):
    model_name = model.__name__
    return model_name[:1].lower() + model_name[1:]


def _get_output_fields(model, return_field_name):
    model_type = _registry.get_type_for_model(model)
    if not model_type:  # pragma: no cover
        raise ImproperlyConfigured(
            "Unable to find type for model {} in graphene registry".format(
                model.__name__,
            )
        )
    f = graphene.Field(
        lambda: _registry.get_type_for_model(model),
        description="The mutated object.",
    )
    return {return_field_name: f}


def _get_validation_errors(validation_error):
    e_list = []

    if hasattr(validation_error, "error_dict"):
        # convert field errors
        for field, field_errors in validation_error.message_dict.items():
            for e in field_errors:
                if field == NON_FIELD_ERRORS:
                    field = None
                else:
                    field = to_camel_case(field)
                e_list.append(MutationErrorType(field=field, message=e))
    else:
        # convert non-field errors
        for e in validation_error.error_list:
            e_list.append(MutationErrorType(message=e.message))

    return e_list


def _get_fields(model, only_fields, exclude_fields, required_fields):
    ret = collections.OrderedDict()
    for name, field in get_model_fields(model):
        if (
            (only_fields and name not in only_fields)
            or name in exclude_fields
            or str(name).endswith("+")
            or name in ["created_at", "updated_at", "archived_at"]
        ):
            continue

        if name == "id":
            f = graphene.ID(
                description="The ID of the object.",
            )
        elif isinstance(field, models.FileField):
            f = UploadType(
                description=field.help_text,
            )
        elif isinstance(field, models.BooleanField):
            f = graphene.Boolean(
                description=field.help_text,
            )
        elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
            f = graphene.ID(
                description=field.help_text,
            )
        elif isinstance(field, models.ManyToManyField):
            f = graphene.List(
                graphene.ID,
                description=field.help_text,
            )
        elif isinstance(field, (ManyToOneRel, ManyToManyRel)):
            reverse_rel_include = graphene_django_plus_settings.MUTATIONS_INCLUDE_REVERSE_RELATIONS
            # Checking whether it was globally configured to not include reverse relations
            if isinstance(field, ManyToOneRel) and not reverse_rel_include and not only_fields:
                continue

            f = graphene.List(
                graphene.ID,
                description="Set list of {}".format(
                    field.related_model._meta.verbose_name_plural,
                ),
            )
        else:
            f = convert_django_field_with_choices(field, _registry)

        if required_fields is not None:
            f.kwargs["required"] = name in required_fields
        else:
            if isinstance(field, (ManyToOneRel, ManyToManyRel)):
                f.kwargs["required"] = not field.null
            else:
                f.kwargs["required"] = not field.blank and field.default is NOT_PROVIDED

        s = schema_for_field(field, name)
        s["validation"]["required"] = f.kwargs["required"]

        ret[name] = {
            "field": f,
            "schema": s,
        }

    return ret


def _is_list_of_ids(field):
    return isinstance(field.type, graphene.List) and field.type.of_type == graphene.ID


def _is_id_field(field):
    return (
        field.type == graphene.ID
        or isinstance(field.type, graphene.NonNull)
        and field.type.of_type == graphene.ID
    )


def _is_upload_field(field):
    t = getattr(field.type, "of_type", field.type)
    return t == UploadType


class BaseMutationOptions(MutationOptions):
    """Model type options for :class:`BaseMutation` and subclasses."""

    #: A list of Django permissions to check against the user
    permissions: Optional[List[str]] = None

    #: If any permission should allow the user to execute this mutation
    permissions_any: bool = True

    #: If we should allow unauthenticated users to do this mutation
    allow_unauthenticated: bool = False

    #: The input schema for the schema query
    input_schema: Optional[dict] = None


class BaseMutation(ClientIDMutation):
    """Base mutation enchanced with permission checking and relay id handling."""

    class Meta:
        abstract = True

    #: A list of errors that happened during the mutation
    errors = graphene.List(
        graphene.NonNull(MutationErrorType),
        description="List of errors that occurred while executing the mutation.",
    )

    @classmethod
    def __class_getitem__(cls, *args, **kwargs):
        return cls

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        permissions=None,
        permissions_any=True,
        allow_unauthenticated=False,
        input_schema=None,
        _meta=None,
        **kwargs,
    ):
        if not _meta:
            _meta = BaseMutationOptions(cls)

        _meta.permissions = permissions or []
        _meta.permissions_any = permissions_any
        _meta.allow_unauthenticated = allow_unauthenticated
        _meta.input_schema = input_schema or {}

        super().__init_subclass_with_meta__(_meta=_meta, **kwargs)

        iname = cls.Input._meta.name
        schema_registry[iname] = {
            "object_type": iname,
            "fields": list(_meta.input_schema.values()),
        }

    @classmethod
    def get_node(cls, info, node_id, field="id", only_type=None):
        """Get the node object given a relay global id."""
        if not node_id:
            return None

        try:
            node = get_node(node_id, only_type)
        except (AssertionError, GraphQLError) as e:
            raise ValidationError({field: str(e)})
        else:
            if node is None:  # pragma: no cover
                raise ValidationError({field: "Couldn't resolve to a node: {}".format(node_id)})

        return node

    @classmethod
    def get_nodes(cls, ids, field, only_type=None):
        """Get a list of node objects given a list of relay global ids."""
        try:
            instances = get_nodes(ids, only_type)
        except GraphQLError as e:
            raise ValidationError({field: str(e)})

        return instances

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
    def mutate_and_get_payload(cls: Type[_M], root, info, **data) -> _M:
        """Mutate checking permissions.

        We override the default graphene's method to call
        :meth:`.check_permissions` and populate :attr:`.errors` in case
        of errors automatically.

        The mutation itself should be defined in :meth:`.perform_mutation`.
        """
        try:
            if not cls.check_permissions(info.context.user):
                raise PermissionDenied()

            response = cls.perform_mutation(root, info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            errors = _get_validation_errors(e)
            return cls(errors=errors)
        except DJPermissionDenied as e:
            if not graphene_django_plus_settings.MUTATIONS_SWALLOW_PERMISSION_DENIED:
                raise
            msg = str(e) or "Permission denied..."
            return cls(errors=[MutationErrorType(message=msg)])

    @classmethod
    def perform_mutation(cls: Type[_M], root, info, **data) -> _M:
        """Perform the mutation.

        This should be implemented in subclasses to perform the mutation.
        """
        raise NotImplementedError


class ModelMutationOptions(BaseMutationOptions):
    """Model type options for :class:`BaseModelMutation` and subclasses."""

    #: The Django model.
    model: Optional[models.Model] = None

    #: A list of guardian object permissions to check if the user has
    #: permission to perform a mutation to the model object.
    object_permissions: Optional[List[str]] = None

    #: If any object permission should allow the user to perform the mutation.
    object_permissions_any: bool = True

    #: Exclude the given fields from the mutation input.
    exclude_fields: Optional[List[str]] = None

    #: Include only those fields in the mutation input.
    only_fields: Optional[List[str]] = None

    #: Mark those fields as required (note that fields marked with `null=False`
    #: in Django will already be considered required).
    required_fields: Optional[List[str]] = None

    #: The name of the field that will contain the object type. If not
    #: provided, it will default to the model's name.
    return_field_name: Optional[str] = None


class BaseModelMutation(BaseMutation, Generic[_T]):
    """Base mutation for models.

    This will allow mutations for both create and update operations,
    depending on if the object's id is present in the input or not.

    See :class:`ModelMutationOptions` for a list of meta configurations.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        object_permissions=None,
        object_permissions_any=True,
        return_field_name=None,
        required_fields=None,
        exclude_fields=None,
        only_fields=None,
        input_schema=None,
        _meta=None,
        **kwargs,
    ):
        if not model:  # pragma: no cover
            raise ImproperlyConfigured("model is required for ModelMutation")
        if not _meta:
            _meta = ModelMutationOptions(cls)

        exclude_fields = exclude_fields or []
        only_fields = only_fields or []
        if not return_field_name:
            return_field_name = _get_model_name(model)

        fdata = _get_fields(model, only_fields, exclude_fields, required_fields)
        input_fields = yank_fields_from_attrs(
            {k: v["field"] for k, v in fdata.items()},
            _as=graphene.InputField,
        )

        input_schema = update_dict_nested(
            {k: v["schema"] for k, v in fdata.items()},
            input_schema or {},
        )

        fields = _get_output_fields(model, return_field_name)

        _meta.model = model
        _meta.object_permissions = object_permissions or []
        _meta.object_permissions_any = object_permissions_any
        _meta.return_field_name = return_field_name
        _meta.exclude_fields = exclude_fields
        _meta.only_fields = only_fields
        _meta.required_fields = required_fields

        super().__init_subclass_with_meta__(
            _meta=_meta,
            input_fields=input_fields,
            input_schema=input_schema,
            **kwargs,
        )

        cls._meta.fields.update(fields)

    @classmethod
    def check_object_permissions(cls, user: Union[AbstractUser, AnonymousUser], instance) -> bool:
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

    @classmethod
    def get_instance(cls, info, obj_id: str) -> _T:
        """Get an object given a relay global id."""
        model_type = _registry.get_type_for_model(cls._meta.model)
        instance = cls.get_node(info, obj_id, only_type=model_type)
        if not cls.check_object_permissions(info.context.user, instance):
            raise PermissionDenied()
        return cast(_T, instance)

    @classmethod
    def before_save(cls, info, instance: _T, cleaned_input: Optional[dict] = None):
        """Perform "before save" operations.

        Override this to perform any operation on the instance
        before its `.save()` method is called.
        """
        pass

    @classmethod
    def after_save(cls, info, instance: _T, cleaned_input: Optional[dict] = None):
        """Perform "after save" operations.

        Override this to perform any operation on the instance
        after its `.save()` method is called.
        """
        pass

    @classmethod
    def save(cls, info, instance: _T, cleaned_input: Optional[dict] = None):
        """Save the instance to the database.

        To do something with the instance "before" or "after" saving it,
        override either :meth:`.before_save` and/or :meth:`.after_save`.
        """
        cls.before_save(info, instance, cleaned_input=cleaned_input)
        instance.save()
        cls.after_save(info, instance, cleaned_input=cleaned_input)

    @classmethod
    def before_delete(cls, info, instance: _T):
        """Perform "before delete" operations.

        Override this to perform any operation on the instance
        before its `.delete()` method is called.
        """
        pass

    @classmethod
    def after_delete(cls, info, instance: _T):
        """Perform "after delete" operations.

        Override this to perform any operation on the instance
        after its `.delete()` method is called.
        """
        pass

    @classmethod
    def delete(cls, info, instance: _T):
        """Delete the instance from the database.

        To do something with the instance "before" or "after" deleting it,
        override either :meth:`.before_delete` and/or :meth:`.after_delete`.
        """
        cls.before_delete(info, instance)
        instance.delete()
        cls.after_delete(info, instance)


class ModelOperationMutation(BaseModelMutation[_T]):
    """Base mutation for operations on models.

    Just like a regular :class:`BaseModelMutation`, but this will receive only
    the object's id so an operation can happen to it.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super().__init_subclass_with_meta__(
            only_fields=["id"],
            required_fields=["id"],
            **kwargs,
        )


class ModelMutation(BaseModelMutation[_T]):
    """Create and update mutation for models.

    This will allow mutations for both create and update operations,
    depending on if the object's id is present in the input or not.
    """

    class Meta:
        abstract = True

    @classmethod
    def create_instance(cls, instance: _T, cleaned_data: dict) -> _T:
        """Create a model instance given the already cleaned input data."""
        opts = instance._meta

        for f in opts.fields:
            if not f.editable or isinstance(f, models.AutoField) or f.name not in cleaned_data:
                continue

            data = cleaned_data[f.name]
            if data is None:
                # We want to reset the file field value when None was passed
                # in the input, but `FileField.save_form_data` ignores None
                # values. In that case we manually pass False which clears
                # the file.
                if isinstance(f, models.FileField):
                    data = False
                if not f.null:
                    data = f._get_default()

            f.save_form_data(instance, data)

        return instance

    @classmethod
    def clean_instance(cls, instance: _T, clean_input: dict) -> _T:
        """Validate the instance by calling its `.full_clean()` method."""
        try:
            instance.full_clean(exclude=cls._meta.exclude_fields)
        except ValidationError as e:
            if e.error_dict:
                raise e

        return instance

    @classmethod
    def clean_input(cls, info, instance: _T, data: dict):
        """Clear and normalize the input data."""
        cleaned_input: Dict[str, Any] = {}

        for f_name, f_item in cls.Input._meta.fields.items():
            if f_name not in data:
                continue
            value = data[f_name]

            if value is not None and _is_list_of_ids(f_item):
                # list of IDs field
                instances = cls.get_nodes(value, f_name) if value else []
                cleaned_input[f_name] = instances
            elif value is not None and _is_id_field(f_item):
                # ID field
                instance = cls.get_node(info, value, f_name)
                cleaned_input[f_name] = instance
            elif value is not None and _is_upload_field(f_item):
                # uploaded files
                value = info.context.FILES.get(value)
                cleaned_input[f_name] = value
            else:
                # other fields
                cleaned_input[f_name] = value

        return cleaned_input

    @classmethod
    @transaction.atomic
    def perform_mutation(cls: Type[_MM], root, info, **data) -> _MM:
        """Perform the mutation.

        Create or update the instance, based on the existence of the
        `id` attribute in the input data and save it.
        """
        obj_id = data.get("id")
        if obj_id:
            checked_permissions = True
            instance = cls.get_instance(info, obj_id)
        else:
            checked_permissions = False
            instance = cls._meta.model()

        cleaned_input = cls.clean_input(info, instance, data)
        instance = cls.create_instance(instance, cleaned_input)
        cls.clean_instance(instance, cleaned_input)
        cls.save(info, instance, cleaned_input)

        # save m2m and related object's data
        for f in itertools.chain(
            instance._meta.many_to_many,
            instance._meta.related_objects,
            instance._meta.private_fields,
        ):
            if isinstance(f, (ManyToOneRel, ManyToManyRel)):
                # Handle reverse side relationships.
                d = cleaned_input.get(f.related_name or f.name + "_set", None)
                if d is not None:
                    target_field = getattr(instance, f.related_name or f.name + "_set")
                    target_field.set(d)
            elif hasattr(f, "save_form_data"):
                d = cleaned_input.get(f.name, None)
                if d is not None:
                    f.save_form_data(instance, d)

        if not checked_permissions and not cls.check_object_permissions(
            info.context.user,
            instance,
        ):
            # If we did not check permissions when getting the instance,
            # check if here. The model might check the permissions based on
            # some related objects
            raise PermissionDenied()

        return cls(**{cls._meta.return_field_name: instance})


class ModelCreateMutation(ModelMutation[_T]):
    """Create mutation for models.

    A shortcut for defining a :class:`ModelMutation` that already excludes
    the `id` from being required.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", []) or []
        if "id" not in exclude_fields:
            exclude_fields.append("id")
        super().__init_subclass_with_meta__(
            exclude_fields=exclude_fields,
            **kwargs,
        )


class ModelUpdateMutation(ModelMutation[_T]):
    """Update mutation for models.

    A shortcut for defining a :class:`ModelMutation` that already enforces
    the `id` to be required.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        if "only_fields" in kwargs and "id" not in kwargs["only_fields"]:
            kwargs["only_fields"].insert(0, "id")
        required_fields = kwargs.pop("required_fields", []) or []
        if "id" not in required_fields:
            required_fields.insert(0, "id")
        super().__init_subclass_with_meta__(
            required_fields=required_fields,
            **kwargs,
        )


class ModelDeleteMutation(ModelOperationMutation[_T]):
    """Delete mutation for models."""

    class Meta:
        abstract = True

    @classmethod
    @transaction.atomic
    def perform_mutation(cls: Type[_MM], root, info, **data) -> _MM:
        """Perform the mutation.

        Delete the instance from the database given its `id` attribute
        in the input data.
        """
        instance = cls.get_instance(info, data.get("id"))

        db_id = instance.id
        cls.delete(info, instance)

        # After the instance is deleted, set its ID to the original database's
        # ID so that the success response contains ID of the deleted object.
        instance.id = db_id
        return cls(**{cls._meta.return_field_name: instance})


# Compatibility with older versions
BaseModelOperationMutation = ModelOperationMutation
