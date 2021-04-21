import graphene
from graphene import relay
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter import DjangoFilterConnectionField


class CountableConnection(relay.Connection):
    """Connection that provides a total_count attribute."""

    class Meta:
        abstract = True

    #: Total objects count in the query.
    total_count = graphene.Int(
        description="The total count of objects in this query.",
    )

    def resolve_total_count(root, info, **kwargs):
        if hasattr(root, "length"):
            return root.length

        return root.iterable.count()


class OrderableConnectionField(DjangoFilterConnectionField):
    """Filter connection with ordering functionality."""

    def __init__(self, *args, **kwargs):
        return super().__init__(
            *args,
            **kwargs,
            orderby=graphene.List(
                graphene.String,
                required=False,
                description="Sort results by field.",
            ),
        )

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        qs = super().resolve_queryset(
            connection,
            iterable,
            info,
            args,
            filtering_args,
            filterset_class,
        )

        order = args.pop("orderby", None) or []
        if order:
            qs = qs.order_by(*[to_snake_case(o) for o in order])

        return qs
