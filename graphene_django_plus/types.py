import types

from django.db import models
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


class MutationErrorType(graphene.ObjectType):
    """An error that happened in a mutation."""

    field = graphene.String(
        description=("The field that caused the error, or `null` if it "
                     "isn't associated with any a particular field."),
        required=False,
    )
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
    """Model type options for :ModelType:."""

    allow_unauthenticated = False
    permissions = None
    object_permissions = None
    object_permissions_any = True


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
                                    **kwargs):
        if not _meta:
            _meta = DjangoObjectTypeOptions(cls)

        _meta.permissions = permissions or []
        _meta.object_permissions = object_permissions or []
        _meta.object_permissions_any = object_permissions_any
        _meta.allow_unauthenticated = allow_unauthenticated

        # Automatic prefetch optimization
        if gql_optimizer is not None:
            prefetch = kwargs.pop('prefetch', {}) or {}
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
        if not cls.check_permissions(info.context.user):
            raise PermissionDenied()

        if (cls._meta.object_permissions and
                hasattr(cls._meta.model.objects, 'for_user')):
            if isinstance(qs, models.Manager):
                qs = qs.get_queryset()
            qs &= cls._meta.model.objects.for_user(
                info.context.user,
                cls._meta.object_permissions,
                any_perm=cls._meta.object_permissions_any,
            )

        ret = super().get_queryset(qs, info)
        if gql_optimizer is None:
            return ret

        return gql_optimizer.query(ret, info)

    @classmethod
    def get_node(cls, info, id):
        instance = super().get_node(info, id)

        if not cls.check_object_permissions(info.context.user, instance):
            raise PermissionDenied()

        return instance

    @classmethod
    def check_permissions(cls, user):
        if not cls._meta.allow_unauthenticated and not user.is_authenticated:
            return False

        if not cls._meta.permissions:
            return True

        return user.has_perms(cls._meta.permissions)

    @classmethod
    def check_object_permissions(cls, user, instance):
        if not hasattr(instance, 'has_perm'):
            return True

        return instance.has_perm(
            user,
            cls._meta.object_permissions,
            any_perm=cls._meta.object_permissions_any,
        )
