import datetime
from typing import List

from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase
from guardian.shortcuts import assign_perm

from .models import Issue, IssueComment, Milestone, Project
from .schema import schema


class BaseTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    user: User
    project: Project
    milestone_1: Milestone
    milestone_2: Milestone
    issues: List[Issue]
    allowed_issues: List[Issue]
    unallowed_issues: List[Issue]
    issues_comments: List[IssueComment]
    unallowed_issues_comments: List[IssueComment]
    allowed_issues_comments: List[IssueComment]

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
                name=f"Issue {i + 1}",
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

        self.issues_comments = []
        self.allowed_issues_comments = []
        self.unallowed_issues_comments = []
        for n, i in enumerate(self.issues):
            for j in range(3):
                c = IssueComment.objects.create(issue=i, comment=f"{i}: {n}-{j} comment")
                self.issues_comments.append(c)
                if i in self.allowed_issues:
                    self.allowed_issues_comments.append(c)
                else:
                    self.unallowed_issues_comments.append(c)
