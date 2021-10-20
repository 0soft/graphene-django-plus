try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

import itertools
from typing import List, Optional

from django.db import models
from django.db.models.fields.reverse_related import ManyToOneRel
import graphene
from graphene.types.mountedtype import MountedType
from graphene.types.objecttype import ObjectType
from graphene.types.structures import Structure
from graphene.types.unmountedtype import UnmountedType
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.registry import get_global_registry
from graphene_django.types import DjangoObjectType
from graphql.error import GraphQLError
from graphql_relay import from_global_id

_registry = get_global_registry()
_extra_register = {}
_input_registry = {}


def _resolve_nodes(ids, graphene_type=None):
    pks = []
    invalid_ids = []
    used_type = graphene_type

    for graphql_id in ids:
        if not graphql_id:
            continue

        try:
            node_type, _id = from_global_id(graphql_id)
        except Exception:
            invalid_ids.append(graphql_id)
            continue

        if used_type and str(used_type) != node_type:  # pragma: nocover
            raise AssertionError("Must receive a {} id.".format(str(used_type)))

        used_type = node_type
        pks.append(_id)

    if invalid_ids:  # pragma: no cover
        raise GraphQLError(
            "Could not resolve to a node with the id list of '{}'.".format(
                invalid_ids,
            ),
        )

    return used_type, pks


def _resolve_graphene_type(type_name):
    for _, _type in itertools.chain(_extra_register.items(), _registry._registry.items()):
        if _type._meta.name == type_name:
            return _type
    else:  # pragma: no cover
        raise AssertionError("Could not resolve the type {}".format(type_name))


def _get_input_attrs(object_type):
    new = {}

    for attr, value in object_type.__dict__.items():
        if not isinstance(value, (MountedType, UnmountedType)):
            continue

        if isinstance(value, Structure) and issubclass(value.of_type, ObjectType):  # type:ignore
            value = type(value)(_input_registry[value.of_type])
        elif isinstance(value, ObjectType):
            value = _input_registry[value.of_type]

        new[attr] = value

    return yank_fields_from_attrs(new, _as=graphene.InputField)


def register_type(graphene_type, name: Optional[str] = None):
    """Register an extra type to be resolved in mutations."""
    assert issubclass(graphene_type, graphene.ObjectType)
    if name is None:
        name = graphene_type._meta.name
    _extra_register[name] = graphene_type
    return graphene_type


def get_node(info, id_: str, graphene_type: Optional[ObjectType] = None):
    """Get a node given the relay id."""
    node_type, _id = from_global_id(id_)
    if not graphene_type:
        graphene_type = _resolve_graphene_type(node_type)
    assert graphene_type is not None

    if issubclass(graphene_type, DjangoObjectType):
        return graphene_type._meta.model.objects.get(pk=_id)
    else:
        return graphene_type.get_node(info, _id)


def get_nodes(info, ids: List[str], graphene_type: Optional[ObjectType] = None):
    """Get a list of nodes.

    If the `graphene_type` argument is provided, the IDs will be validated
    against this type. If the type was not provided, it will be looked up in
    the Graphene's registry.

    Raises an error if not all IDs are of the same type.
    """
    if not ids:  # pragma: nocover
        raise ValueError("ids list cannot be empty")

    nodes_type, pks = _resolve_nodes(ids, graphene_type)

    # If `graphene_type` was not provided, check if all resolved types are
    # the same. This prevents from accidentally mismatching IDs of different
    # types.
    if nodes_type and not graphene_type:
        graphene_type = _resolve_graphene_type(nodes_type)
    assert graphene_type is not None

    if issubclass(graphene_type, DjangoObjectType):
        nodes = list(graphene_type._meta.model.objects.filter(pk__in=pks))
        nodes.sort(key=lambda e: pks.index(str(e.pk)))  # preserve order in pks

        diff = set(pks) - {str(n.pk) for n in nodes}
        if diff:
            raise GraphQLError(
                "There is no node of type {} with pk {}".format(
                    graphene_type,
                    ", ".join(diff),
                )
            )
    else:
        nodes = [graphene_type.get_node(info, id_) for id_ in pks]

    return nodes


def get_inputtype(name, object_type):
    """Get an input type based on the object type"""
    if object_type in _input_registry:
        return _input_registry[object_type]

    inputtype = type(
        name,
        (graphene.InputObjectType,),
        _get_input_attrs(object_type),
    )

    _input_registry[object_type] = inputtype
    return inputtype


def get_model_fields(model: models.Model):
    fields = [
        (field.name, field)
        for field in sorted(model._meta.fields + model._meta.many_to_many)  # type:ignore
    ]
    fields.extend(
        [
            (field.related_name or field.name + "_set", field)
            for field in sorted(
                model._meta.related_objects,
                key=lambda field: field.name,
            )
            if not isinstance(field, ManyToOneRel) or field.remote_field.null
        ],
    )
    return fields


def update_dict_nested(d: dict, u: dict) -> dict:
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = update_dict_nested(d.get(k, {}), v)  # type:ignore
        else:
            d[k] = v

    return d
