import graphene
from graphene import relay
from graphene_django.registry import Registry

from graphene_django_plus.fields import CountableConnection, OrderableConnectionField
from graphene_django_plus.mutations import (
    ModelCreateMutation,
    ModelDeleteMutation,
    ModelUpdateMutation,
)
from graphene_django_plus.queries import Query as _Query
from graphene_django_plus.types import ModelType

from .models import Issue, Milestone, MilestoneComment, Project

# Registry

project_name_only_registry = Registry()

# Types


class IssueType(ModelType):
    class Meta:
        model = Issue
        connection_class = CountableConnection
        interfaces = [relay.Node]
        object_permissions = [
            "can_read",
        ]
        filter_fields = {}


class MilestoneType(ModelType):
    class Meta:
        model = Milestone
        connection_class = CountableConnection
        interfaces = [relay.Node]
        filter_fields = {}


class ProjectType(ModelType):
    class Meta:
        model = Project
        connection_class = CountableConnection
        interfaces = [relay.Node]
        filter_fields = {}


class MilestoneCommentType(ModelType):
    class Meta:
        model = MilestoneComment
        connection_class = CountableConnection
        interfaces = [relay.Node]
        filter_fields = {}


class ProjectNameOnlyType(ModelType):
    class Meta:
        model = Project
        fields = ["id", "name"]
        connection_class = CountableConnection
        interfaces = [relay.Node]
        filter_fields = {}
        registry = project_name_only_registry


# Queries


class Query(graphene.ObjectType, _Query):
    projects = OrderableConnectionField(ProjectType)
    project = relay.Node.Field(ProjectType)
    project_name_only = relay.Node.Field(ProjectNameOnlyType)

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
            "can_write",
        ]


class IssueDeleteMutation(ModelDeleteMutation):
    class Meta:
        model = Issue
        object_permissions = [
            "can_write",
        ]


class ProjectNameOnlyUpdateMutation(ModelUpdateMutation):
    class Meta:
        model = Project
        registry = project_name_only_registry


class Mutation(graphene.ObjectType):
    """Milestones mutation."""

    project_create = ProjectCreateMutation.Field()
    project_update = ProjectUpdateMutation.Field()
    project_delete = ProjectDeleteMutation.Field()
    project_update_name = ProjectNameOnlyUpdateMutation.Field()

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
