# This was based on some code from https://github.com/mirumee/saleor
# but adapted to use relay, automatic field detection and some code adjustments

import collections
import itertools

from django.core.exceptions import (
    NON_FIELD_ERRORS,
    ImproperlyConfigured,
    ValidationError,
)
from django.db import (
    models,
    transaction,
)
import graphene
from graphene.relay.mutation import ClientIDMutation
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.registry import get_global_registry
from graphene_django.converter import convert_django_field_with_choices
from graphql.error import GraphQLError

from .exceptions import PermissionDenied
from .types import (
    MutationErrorType,
    UploadType,
)
from .utils import (
    get_nodes,
    snake2camelcase,
)

_registry = get_global_registry()


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
    f = graphene.Field(model_type, description="The mutated object.")
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
                    field = snake2camelcase(field)
                e_list.append(MutationErrorType(field=field, message=e))
    else:
        # convert non-field errors
        for e in validation_error.error_list:
            e_list.append(MutationErrorType(message=e.message))

    return e_list


def _get_fields(model, only_fields, exclude_fields, required_fields):
    fields = [
        (field.name, field)
        for field in sorted(list(model._meta.fields))
    ]

    ret = collections.OrderedDict()
    for name, field in fields:
        if ((only_fields and name not in only_fields) or
                name in exclude_fields or
                str(name).endswith('+') or
                name in ['created_at', 'updated_at', 'archived_at']):
            continue

        if name == 'id':
            ret[name] = graphene.ID(
                description="The ID of the object.",
            )
        elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
            ret[name] = graphene.ID(
                description=field.help_text,
                required=not field.null,
            )
        else:
            ret[name] = convert_django_field_with_choices(field, _registry)

        if required_fields is not None:
            ret[name].kwargs['required'] = name in required_fields

    return ret


def _is_list_of_ids(field):
    return (
        isinstance(field.type, graphene.List) and
        field.type.of_type == graphene.ID
    )


def _is_id_field(field):
    return (
        field.type == graphene.ID or
        isinstance(field.type, graphene.NonNull) and
        field.type.of_type == graphene.ID
    )


def _is_upload_field(field):
    t = getattr(field.type, 'of_type', field.type)
    return t == UploadType


class BaseMutationOptions(MutationOptions):
    """Model type options for :BaseMutation: and subclasses."""

    permissions = None
    allow_unauthenticated = False


class BaseMutation(ClientIDMutation):
    """Base mutation enchanced with permission checking and relay id handling."""

    class Meta:
        abstract = True

    errors = graphene.List(
        graphene.NonNull(MutationErrorType),
        description="List of errors that occurred while executing the mutation.",
    )

    @classmethod
    def __init_subclass_with_meta__(cls, permissions=None,
                                    allow_unauthenticated=False,
                                    _meta=None, **kwargs):
        if not _meta:
            _meta = BaseMutationOptions(cls)

        _meta.permissions = permissions or []
        _meta.allow_unauthenticated = allow_unauthenticated

        super().__init_subclass_with_meta__(_meta=_meta, **kwargs)

    @classmethod
    def get_node(cls, info, node_id, field='id', only_type=None):
        if not node_id:
            return None

        try:
            node = graphene.Node.get_node_from_global_id(
                info,
                node_id,
                only_type,
            )
        except (AssertionError, GraphQLError) as e:
            raise ValidationError({field: str(e)})
        else:
            if node is None:  # pragma: no cover
                raise ValidationError(
                    {field: "Couldn't resolve to a node: {}".format(node_id)}
                )

        return node

    @classmethod
    def get_nodes(cls, ids, field, only_type=None):
        try:
            instances = get_nodes(ids, only_type)
        except GraphQLError as e:
            raise ValidationError({field: str(e)})

        return instances

    @classmethod
    def check_permissions(cls, user):
        if not cls._meta.allow_unauthenticated and not user.is_authenticated:
            return False

        if not cls._meta.permissions:
            return True

        return user.has_perms(cls._meta.permissions)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        if not cls.check_permissions(info.context.user):
            raise PermissionDenied()

        try:
            response = cls.perform_mutation(root, info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            errors = _get_validation_errors(e)
            return cls(errors=errors)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass


class ModelMutationOptions(BaseMutationOptions):
    """Model type options for :BaseModelMutation: and subclasses."""

    object_permissions = None
    object_permissions_any = True
    exclude_fields = None
    only_fields = None
    required_fields = None
    model = None
    return_field_name = None


class BaseModelMutation(BaseMutation):
    """Base mutation for models.

    This will allow mutations for both create and update operations,
    depending on if the object's id is present in the input or not.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, model=None,
                                    object_permissions=None,
                                    object_permissions_any=True,
                                    return_field_name=None,
                                    required_fields=None,
                                    exclude_fields=None, only_fields=None,
                                    _meta=None, **kwargs):
        if not model:  # pragma: no cover
            raise ImproperlyConfigured("model is required for ModelMutation")
        if not _meta:
            _meta = ModelMutationOptions(cls)

        exclude_fields = exclude_fields or []
        only_fields = only_fields or []
        if not return_field_name:
            return_field_name = _get_model_name(model)

        input_fields = _get_fields(model, only_fields, exclude_fields,
                                   required_fields)
        input_fields = yank_fields_from_attrs(input_fields, _as=graphene.InputField)

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
            **kwargs,
        )

        cls._meta.fields.update(fields)

    @classmethod
    def check_object_permissions(cls, user, instance):
        if not hasattr(instance, 'has_perm'):
            return True

        return instance.has_perm(
            user,
            cls._meta.object_permissions,
            any_perm=cls._meta.object_permissions_any,
        )

    @classmethod
    def get_instance(cls, info, obj_id):
        model_type = _registry.get_type_for_model(cls._meta.model)
        instance = cls.get_node(info, obj_id, only_type=model_type)
        if not cls.check_object_permissions(info.context.user, instance):
            raise PermissionDenied()
        return instance

    @classmethod
    def before_save(cls, info, instance, cleaned_input=None):
        pass

    @classmethod
    def after_save(cls, info, instance, cleaned_input=None):
        pass

    @classmethod
    def save(cls, info, instance, cleaned_input=None):
        cls.before_save(info, instance, cleaned_input=cleaned_input)
        instance.save()
        cls.after_save(info, instance, cleaned_input=cleaned_input)

    @classmethod
    def before_delete(cls, info, instance):
        pass

    @classmethod
    def after_delete(cls, info, instance):
        pass

    @classmethod
    def delete(cls, info, instance):
        cls.before_delete(info, instance)
        instance.delete()
        cls.after_delete(info, instance)


class BaseModelOperationMutation(BaseModelMutation):
    """Base mutation for operations on models.

    Just like a regular BaseModelMutation, but this will receive only
    the object's id so an operation can happen to it.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super().__init_subclass_with_meta__(
            only_fields=['id'],
            required_fields=['id'],
            **kwargs,
        )


class ModelMutation(BaseModelMutation):
    """Create and update mutation for models.

    This will allow mutations for both create and update operations,
    depending on if the object's id is present in the input or not.
    """

    class Meta:
        abstract = True

    @classmethod
    def create_instance(cls, instance, cleaned_data):
        opts = instance._meta

        for f in opts.fields:
            if (not f.editable or
                    isinstance(f, models.AutoField) or
                    f.name not in cleaned_data):
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
    def clean_instance(cls, instance, clean_input):
        try:
            instance.full_clean()
        except ValidationError as e:
            if e.error_dict:
                raise e

        return instance

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = {}

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
    def perform_mutation(cls, root, info, **data):
        obj_id = data.get('id')
        if obj_id:
            instance = cls.get_instance(info, obj_id)
        else:
            instance = cls._meta.model()

        cleaned_input = cls.clean_input(info, instance, data)
        instance = cls.create_instance(instance, cleaned_input)
        cls.clean_instance(instance, cleaned_input)
        cls.save(info, instance, cleaned_input)

        # save m2m data
        for f in itertools.chain(instance._meta.many_to_many,
                                 instance._meta.private_fields):
            if not hasattr(f, 'save_form_data'):
                continue

            d = cleaned_input.get(f.name, None)
            if d is not None:
                f.save_form_data(instance, d)

        return cls(**{cls._meta.return_field_name: instance})


class ModelCreateMutation(ModelMutation):
    """Create mutation for models.

    A shortcut for defining a :ModelMutation: that already excludes
    the `id` from being required.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', []) or []
        if 'id' not in exclude_fields:
            exclude_fields.append('id')
        super().__init_subclass_with_meta__(
            exclude_fields=exclude_fields,
            **kwargs,
        )


class ModelUpdateMutation(ModelMutation):
    """Update mutation for models.

    A shortcut for defining a :ModelMutation: that already enforces
    the `id` to be required.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        required_fields = kwargs.pop('required_fields', []) or []
        if 'id' not in required_fields:
            required_fields.append('id')
        super().__init_subclass_with_meta__(
            required_fields=required_fields,
            **kwargs,
        )


class ModelDeleteMutation(BaseModelOperationMutation):
    """Delete mutation for models."""

    class Meta:
        abstract = True

    @classmethod
    @transaction.atomic
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, data.get('id'))

        db_id = instance.id
        cls.delete(info, instance)

        # After the instance is deleted, set its ID to the original database's
        # ID so that the success response contains ID of the deleted object.
        instance.id = db_id
        return cls(**{cls._meta.return_field_name: instance})
