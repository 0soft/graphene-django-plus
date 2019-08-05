import base64
import json
from unittest import mock

from guardian.shortcuts import assign_perm

from .base import BaseTestCase
from .models import (
    Project,
    Milestone,
    Issue,
)


class TestTypes(BaseTestCase):

    def test_mutation_create(self):
        # project
        self.assertIsNone(Project.objects.filter(name='FooBar').first())
        r = self.query(
            """
            mutation {
              projectCreate (input: {name: "FooBar"}) {
                project {
                  name
                }
              }
            }
            """,
            op_name='projectCreate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'projectCreate': {'project': {'name': 'FooBar'}}}},
        )
        self.assertIsNotNone(Project.objects.filter(name='FooBar').first())

        # milestone
        p_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        self.assertIsNone(Milestone.objects.filter(name='BarBin').first())
        r = self.query(
            """
            mutation {
              milestoneCreate (input: {name: "BarBin", project: "%s"}) {
                milestone {
                  name
                  project {
                    name
                  }
                }
              }
            }
            """ % (p_id, ),
            op_name='milestoneCreate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'milestoneCreate': {
                    'milestone': {
                        'name': 'BarBin',
                        'project': {
                            'name': 'Test Project'
                        }
                    }
                }
            }},
        )
        self.assertIsNotNone(Milestone.objects.filter(name='BarBin').first())

    def test_mutation_update(self):
        # project
        p_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        self.assertNotEqual(self.project.name, "XXX")
        r = self.query(
            """
            mutation {
              projectUpdate (input: {id: "%s" name: "XXX"}) {
                project {
                  name
                }
              }
            }
            """ % (p_id, ),
            op_name='projectUpdate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'projectUpdate': {'project': {'name': 'XXX'}}}},
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "XXX")

        # issue (allowed)
        issue = self.allowed_issues[0]
        i_id = base64.b64encode('IssueType:{}'.format(
            issue.id,
        ).encode()).decode()
        self.assertNotEqual(issue.name, "YYY")
        r = self.query(
            """
            mutation {
              issueUpdate (input: {id: "%s" name: "YYY"}) {
                issue {
                  name
                }
              }
            }
            """ % (i_id, ),
            op_name='issueUpdate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'issueUpdate': {'issue': {'name': 'YYY'}}}},
        )
        issue.refresh_from_db()
        self.assertEqual(issue.name, "YYY")

        # issue (not allowed)
        issue = self.unallowed_issues[0]
        i_id = base64.b64encode('IssueType:{}'.format(
            issue.id,
        ).encode()).decode()
        r = self.query(
            """
            mutation {
              issueUpdate (input: {id: "%s" name: "YYY"}) {
                issue {
                  name
                }
              }
            }
            """ % (i_id, ),
            op_name='issueUpdate',
        )
        self.assertResponseHasErrors(r)

    def test_mutation_delete(self):
        # project
        p_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        r = self.query(
            """
            mutation {
              projectDelete (input: {id: "%s"}) {
                project {
                  name
                }
              }
            }
            """ % (p_id, ),
            op_name='projectDelete',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'projectDelete': {'project': {'name': 'Test Project'}}}},
        )
        self.assertIsNone(Project.objects.filter(id=self.project.id).first())

        # issue (allowed)
        issue = self.allowed_issues[0]
        i_id = base64.b64encode('IssueType:{}'.format(
            issue.id,
        ).encode()).decode()
        r = self.query(
            """
            mutation {
              issueDelete (input: {id: "%s"}) {
                issue {
                  name
                }
              }
            }
            """ % (i_id, ),
            op_name='issueDelete',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'issueDelete': {'issue': {'name': issue.name}}}},
        )
        self.assertIsNone(Issue.objects.filter(id=issue.id).first())

        # issue (not allowed)
        issue = self.unallowed_issues[0]
        i_id = base64.b64encode('IssueType:{}'.format(
            issue.id,
        ).encode()).decode()
        r = self.query(
            """
            mutation {
              issueDelete (input: {id: "%s"}) {
                issue {
                  name
                }
              }
            }
            """ % (i_id, ),
            op_name='issueDelete',
        )
        self.assertResponseHasErrors(r)
