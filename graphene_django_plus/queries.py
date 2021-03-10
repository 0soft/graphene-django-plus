import graphene

from .mutations import input_schema_registry
from .types import InputSchemaType


class Query(object):
    """Queries object."""

    gql_input_schema = graphene.Field(
        InputSchemaType,
        description="GraphQL input schema for forms.",
        input_object=graphene.String(
            description="The input object to query for.",
            required=True,
        ),
        required=False,
        default_value=None,
    )
    gql_input_schema_all = graphene.List(
        graphene.NonNull(InputSchemaType),
        description="GraphQL input schema for forms.",
        required=True,
    )

    def resolve_gql_input_schema(root, info, input_object, **kwargs):
        return input_schema_registry.get(input_object, None)

    def resolve_gql_input_schema_all(root, info, **kwargs):
        return sorted(
            input_schema_registry.values(), key=lambda obj: obj["input_object"]
        )
