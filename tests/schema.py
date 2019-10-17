import graphene
from graphene import relay

from graphene_django_plus.types import ModelType
from graphene_django_plus.fields import (
    CountableConnection,
    OrderableConnectionField,
)
from graphene_django_plus.mutations import (
    ModelCreateMutation,
    ModelUpdateMutation,
    ModelDeleteMutation,
)

from .models import (
    Project,
    Milestone,
    Issue,
)

# Types


class IssueType(ModelType):
    class Meta:
        model = Issue
        connection_class = CountableConnection
        interfaces = [relay.Node]
        object_permissions = [
            'can_read',
        ]
        filter_fields = {}


class MilestoneType(ModelType):
    class Meta:
        model = Milestone
        connection_class = CountableConnection
        interfaces = [relay.Node]
        prefetch = {
            'issues': IssueType,
        }
        filter_fields = {}


class ProjectType(ModelType):
    class Meta:
        model = Project
        connection_class = CountableConnection
        interfaces = [relay.Node]
        prefetch = {
            'milestones': MilestoneType,
        }
        filter_fields = {}


# Queries


class Query(graphene.ObjectType):
    projects = OrderableConnectionField(ProjectType)
    project = relay.Node.Field(ProjectType)

    milestones = OrderableConnectionField(MilestoneType)
    milestone = relay.Node.Field(MilestoneType)

    issues = OrderableConnectionField(IssueType)
    issue = relay.Node.Field(IssueType)


# Mutations


class ProjectCreateMutation(ModelCreateMutation):
    class Meta:
        model = Project


class ProjectUpdateMutation(ModelUpdateMutation):
    class Meta:
        model = Project


class ProjectDeleteMutation(ModelDeleteMutation):
    class Meta:
        model = Project


class MilestoneCreateMutation(ModelCreateMutation):
    class Meta:
        model = Milestone


class MilestoneUpdateMutation(ModelUpdateMutation):
    class Meta:
        model = Milestone


class MilestoneDeleteMutation(ModelDeleteMutation):
    class Meta:
        model = Milestone


class IssueCreateMutation(ModelCreateMutation):
    class Meta:
        model = Issue


class IssueUpdateMutation(ModelUpdateMutation):
    class Meta:
        model = Issue
        object_permissions = [
            'can_write',
        ]


class IssueDeleteMutation(ModelDeleteMutation):
    class Meta:
        model = Issue
        object_permissions = [
            'can_write',
        ]


class Mutation(graphene.ObjectType):
    """Milestones mutation."""

    project_create = ProjectCreateMutation.Field()
    project_update = ProjectUpdateMutation.Field()
    project_delete = ProjectDeleteMutation.Field()

    milestone_create = MilestoneCreateMutation.Field()
    milestone_update = MilestoneUpdateMutation.Field()
    milestone_delete = MilestoneDeleteMutation.Field()

    issue_create = IssueCreateMutation.Field()
    issue_update = IssueUpdateMutation.Field()
    issue_delete = IssueDeleteMutation.Field()


# Schema


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
