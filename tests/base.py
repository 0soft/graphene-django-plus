import datetime

from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from guardian.shortcuts import assign_perm

from .schema import schema
from .models import (
    Project,
    Milestone,
    Issue,
)


class BaseTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = User(username="foobar")
        self.user.set_password("foobar")
        self.user.save()
        self.client.login(username="foobar", password="foobar")

        self.project = Project.objects.create(
            name="Test Project",
            due_date=datetime.date(2050, 1, 1),
        )
        self.milestone_1 = Milestone.objects.create(
            name="Milestone 1",
            due_date=datetime.date(2050, 1, 1),
            project=self.project,
        )
        self.milestone_2 = Milestone.objects.create(
            name="Milestone 2",
            project=self.project,
        )
        self.allowed_issues = []
        self.unallowed_issues = []
        self.issues = []
        for i, (priority, milestone) in enumerate(
            [
                (1, self.milestone_1),
                (1, self.milestone_1),
                (0, self.milestone_2),
                (3, None),
            ]
        ):
            i = Issue.objects.create(
                name="Issue {}".format(i + 1),
                priority=priority,
                milestone=milestone,
            )
            if milestone == self.milestone_1:
                assign_perm("can_read", self.user, i)
                assign_perm("can_write", self.user, i)
                self.allowed_issues.append(i)
            else:
                self.unallowed_issues.append(i)

            self.issues.append(i)
