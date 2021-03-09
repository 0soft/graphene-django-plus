import base64

from graphene_django_plus.utils import get_nodes
from .base import BaseTestCase
from .schema import (
    ProjectType,
    IssueType,
)


class TestTypes(BaseTestCase):
    def test_get_nodes(self):
        issues = [
            base64.b64encode(
                "IssueType:{}".format(
                    issue.id,
                ).encode()
            ).decode()
            for issue in self.issues
        ]
        self.assertEqual(
            set(get_nodes(issues)),
            set(self.issues),
        )
        self.assertEqual(
            set(get_nodes(issues, IssueType)),
            set(self.issues),
        )
        with self.assertRaises(AssertionError):
            get_nodes(issues, ProjectType)

        issues_with_wrong_id = issues[:]
        issues_with_wrong_id.append(
            base64.b64encode("IssueType:9999".encode()).decode()
        )
        with self.assertRaises(AssertionError):
            get_nodes(issues_with_wrong_id)
