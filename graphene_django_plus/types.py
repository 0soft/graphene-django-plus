import types

from django.db import models
from django.db.models import Prefetch
import graphene
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectTypeOptions

try:
    import graphene_django_optimizer as gql_optimizer
    _BaseDjangoObjectType = gql_optimizer.OptimizedDjangoObjectType
except ImportError:
    gql_optimizer = None
    _BaseDjangoObjectType = DjangoObjectType

from .exceptions import PermissionDenied
from .models import (
    GuardedModel,
    GuardedModelManager,
)


class MutationErrorType(graphene.ObjectType):
    """An error that happened in a mutation."""

    #: The field that caused the error, or `null` if it isn't associated
    #: with any particular field.
    field = graphene.String(
        description=("The field that caused the error, or `null` if it "
                     "isn't associated with any particular field."),
        required=False,
    )

    #: The error message
    message = graphene.String(description="The error message.")


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
    allow_unauthenticated = False

    #: A list of django permissions to check if the user has permission to
    #: query this model.
    permissions = None

    #: A list of guardian object permissions to check if the user has
    #: permission to query the model object.
    object_permissions = None

    #: If any object permission should allow the user to query this model.
    object_permissions_any = True

    #: A dict defining fields to be prefetched. This should map the
    #: related name to the type. e.g. `{'items': ItemType}`.
    #: Note that for this to work, `graphene_django_optimizer` needs
    #: to be installed
    prefetch = None


class ModelType(_BaseDjangoObjectType):
    """Base type with automatic optimizations and permissions checking."""

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, model=None,
                                    permissions=None,
                                    object_permissions=None,
                                    object_permissions_any=True,
                                    allow_unauthenticated=False,
                                    prefetch=None,
                                    **kwargs):
        if not _meta:
            _meta = DjangoObjectTypeOptions(cls)

        _meta.permissions = permissions or []
        _meta.object_permissions = object_permissions or []
        _meta.object_permissions_any = object_permissions_any
        _meta.allow_unauthenticated = allow_unauthenticated

        # Automatic prefetch optimization
        if gql_optimizer is not None:
            prefetch = prefetch or {}
            for k, v in prefetch.items():
                if isinstance(v, types.FunctionType):
                    v = v()
                f = gql_optimizer.field(
                    DjangoConnectionField(v),
                    model_field=k,
                )
                r = lambda s, i, **kw: getattr(s, k).all()
                setattr(cls, k, f)
                setattr(cls, 'resolve_' + k, r)

        super().__init_subclass_with_meta__(_meta=_meta, model=model, **kwargs)

    @classmethod
    def get_queryset(cls, qs, info):
        """Get the queryset checking for permissions and optimizing the query.

        Override the default graphene's `get_queryset` to check for permissions
        and optimize the query performance.

        Note that the query will only be automaticallu optimized if,
        `graphene_django_optimizer` is installed.
        """
        if not cls.check_permissions(info.context.user):
            raise PermissionDenied("No permissions")

        if isinstance(qs, models.Manager):
            qs = qs.get_queryset()

        if (cls._meta.object_permissions and
                isinstance(cls._meta.model.objects, GuardedModelManager)):
            qs &= cls._meta.model.objects.for_user(
                info.context.user,
                cls._meta.object_permissions,
                any_perm=cls._meta.object_permissions_any,
            )

        ret = super().get_queryset(qs, info)
        if gql_optimizer is None:
            return ret

        ret = gql_optimizer.query(ret, info)
        prl = {i.to_attr if isinstance(i, Prefetch) else i: i
               for i in ret._prefetch_related_lookups}
        ret._prefetch_related_lookups = tuple(prl.values())

        return ret

    @classmethod
    def get_node(cls, info, id):
        """Get the node instance given the relay global id."""
        instance = super().get_node(info, id)

        if not cls.check_object_permissions(info.context.user, instance):
            raise PermissionDenied()

        return instance

    @classmethod
    def check_permissions(cls, user):
        """Check permissions for the given user.

        Subclasses can override this to avoid the permission checking or
        extending it. Remember to call `super()` in the later case.
        """
        if not cls._meta.allow_unauthenticated and not user.is_authenticated:
            return False

        if not cls._meta.permissions:
            return True

        return user.has_perms(cls._meta.permissions)

    @classmethod
    def check_object_permissions(cls, user, instance):
        """Check object permissions for the given user.

        Subclasses can override this to avoid the permission checking or
        extending it. Remember to call `super()` in the later case.

        For this to work, the model needs to implement a `has_perm` method.
        The easiest way when using `guardian` is to inherit it
        from :class:`graphene_django_plus.models.GuardedModel`.
        """
        if not isinstance(instance, GuardedModel):
            return True

        return instance.has_perm(
            user,
            cls._meta.object_permissions,
            any_perm=cls._meta.object_permissions_any,
        )
