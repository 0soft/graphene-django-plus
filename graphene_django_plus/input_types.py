"""
Module that defines the mapping between model fields and GraphQL input types
used in mutations.
"""
import functools
from typing import Union

import graphene
from django.db import models
from django.db.models import Field, ForeignObjectRel
from graphene import Scalar
from graphene.types.structures import Structure
from graphene_django.converter import convert_django_field_with_choices
from graphene_django.registry import Registry

from .types import UploadType


@functools.singledispatch
def get_input_field(field: Union[Field, ForeignObjectRel], registry: Registry) -> Union[Scalar, Structure]:
    """
    Convert a model field into a GraphQL input type used in mutations.
    :param field: A model field.
    :param registry: Registry which holds a mapping between django models/fields
      and Graphene types.
    :return: A scalar that can be used as an input field in mutations.
    """
    return convert_django_field_with_choices(field, registry)


@get_input_field.register(models.FileField)
def get_file_field(field, registry):
    return UploadType(
        description=field.help_text,
    )


@get_input_field.register(models.BooleanField)
def get_boolean_field(field, registry):
    return graphene.Boolean(
        description=field.help_text,
    )


@get_input_field.register(models.ForeignKey)
@get_input_field.register(models.OneToOneField)
def get_foreign_key_field(field, registry):
    return graphene.ID(
        description=field.help_text,
    )


@get_input_field.register(models.ManyToManyField)
def get_many_to_many_field(field, registry):
    return graphene.List(
        graphene.ID,
        description=field.help_text,
    )


@get_input_field.register(models.ManyToOneRel)
@get_input_field.register(models.ManyToManyRel)
def get_relation_field(field, registry):
    return graphene.List(
        graphene.ID,
        description="Set list of {}".format(field.related_model._meta.verbose_name_plural),
    )
