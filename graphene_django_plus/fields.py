import graphene
from graphene import relay


class CountableConnection(relay.Connection):
    """Connection that provides a total_count attribute."""

    class Meta:
        abstract = True

    total_count = graphene.Int(
        description="The total count of objects in this query.",
    )

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()
