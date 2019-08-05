import graphene
from graphene import relay

from graphene_django.fields import DjangoConnectionField
from graphene_django_plus.types import ModelType
from graphene_django_plus.fields import CountableConnection
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


class IssueType(ModelType, interfaces=[relay.Node]):
    class Meta:
        model = Issue
        connection_class = CountableConnection
        object_permissions = [
            'can_read',
        ]


class MilestoneType(ModelType, interfaces=[relay.Node]):
    class Meta:
        model = Milestone
        connection_class = CountableConnection
        prefetch = {
            'issues': IssueType,
        }


class ProjectType(ModelType, interfaces=[relay.Node]):
    class Meta:
        model = Project
        connection_class = CountableConnection
        prefetch = {
            'milestones': MilestoneType,
        }


# Queries


class Query(graphene.ObjectType):
    projects = DjangoConnectionField(ProjectType)
    project = relay.Node.Field(ProjectType)

    milestones = DjangoConnectionField(MilestoneType)
    milestone = relay.Node.Field(MilestoneType)

    issues = DjangoConnectionField(IssueType)
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
