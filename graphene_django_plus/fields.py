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

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


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
    def connection_resolver(cls, resolver, connection, default_manager,
                            max_limit, enforce_first_or_last, filterset_class,
                            filtering_args, root, info, **kwargs):
        filter_kwargs = {k: v for k, v in kwargs.items() if k in filtering_args}
        qs = filterset_class(
            data=filter_kwargs,
            queryset=default_manager.get_queryset(),
            request=info.context,
        ).qs

        order = kwargs.pop('orderby', None) or []

        if order:
            qs = qs.order_by(*[to_snake_case(o) for o in order])

        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver,
            connection,
            qs,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **kwargs
        )

    @classmethod
    def merge_querysets(cls, default_queryset, queryset):
        return queryset
