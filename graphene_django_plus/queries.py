import graphene

from .types import (
    schema_registry,
    SchemaType,
)


class Query(object):
    """Queries object."""

    gql_object_schema = graphene.Field(
        SchemaType,
        description="GraphQL input schema for forms.",
        object_type=graphene.String(
            description="The input object to query for.",
            required=True,
        ),
        required=False,
        default_value=None,
    )
    gql_object_schema_all = graphene.List(
        graphene.NonNull(SchemaType),
        description="GraphQL input schema for forms.",
        required=True,
    )

    def resolve_gql_object_schema(root, info, object_type, **kwargs):
        return schema_registry.get(object_type, None)

    def resolve_gql_object_schema_all(root, info, **kwargs):
        return sorted(schema_registry.values(), key=lambda obj: obj["object_type"])
