import base64

from graphene_django.registry import Registry
from graphql.error.base import GraphQLError

from graphene_django_plus.utils import get_nodes

from .base import BaseTestCase
from .schema import IssueType, ProjectType


class TestTypes(BaseTestCase):
    def test_get_nodes(self):
        info = object()

        issues = [
            base64.b64encode(
                "IssueType:{}".format(
                    issue.id,
                ).encode()
            ).decode()
            for issue in self.issues
        ]
        self.assertEqual(
            set(get_nodes(info, issues)),
            set(self.issues),
        )
        self.assertEqual(
            set(get_nodes(info, issues, IssueType)),
            set(self.issues),
        )
        with self.assertRaises(AssertionError):
            get_nodes(info, issues, ProjectType)

        with self.assertRaises(AssertionError):
            get_nodes(info, issues, registry=Registry())

        issues_with_wrong_id = issues[:]
        issues_with_wrong_id.append(base64.b64encode(b"IssueType:9999").decode())
        with self.assertRaises(GraphQLError):
            get_nodes(info, issues_with_wrong_id)
