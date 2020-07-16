import base64
import json

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
            mutation projectCreate {
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
            mutation milestoneCreate {
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
            mutation projectUpdate {
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
            mutation issueUpdate {
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
            mutation issueUpdate {
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
            mutation projectDelete {
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
            mutation issueDelete {
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
            mutation issueDelete {
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


class TestMutationRelatedObjects(BaseTestCase):
    """Tests for creating and updating reverse side of FK and M2M relationships."""

    def test_create_milestone_issues(self):
        """Test that a milestone can be created with a list of issues."""
        milestone = 'release_1A'
        self.assertIsNone(Milestone.objects.filter(name=milestone).first())

        project_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        issue_id = base64.b64encode('IssueType:{}'.format(
            self.issues[0].id,
        ).encode()).decode()

        r = self.query(
            """
            mutation milestoneCreate {
              milestoneCreate (input: {
                name: "%s",
                project: "%s",
                issues: ["%s"]
              }) {
                milestone {
                  name
                  issues {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
            """ % (milestone, project_id, issue_id),
            op_name='milestoneCreate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'milestoneCreate': {
                  'milestone': {
                    'name': 'release_1A',
                    'issues': {
                      'edges': [{
                        'node': {
                          'name': 'Issue 1'
                        },
                      }]
                    }
                  }
                }
              }
            }
        )
        self.assertIsNotNone(Milestone.objects.filter(name=milestone).first())

    def test_update_milestone_issues(self):
        """Test that issues can be updated as a part of milestone update."""
        milestone = Milestone.objects.create(name='release-A', project=self.project)
        milestone.issues.set(self.issues)
        m_id = base64.b64encode('MilestoneType:{}'.format(
            milestone.id,
        ).encode()).decode()

        # Now update it to just having a single issue.
        issue_id = base64.b64encode('IssueType:{}'.format(
            self.issues[0].id,
        ).encode()).decode()
        r = self.query(
            """
            mutation milestoneUpdate {
              milestoneUpdate (input: {
                id: "%s",
                issues: ["%s"]
              }) {
                milestone {
                  name
                  issues {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
            """ % (m_id, issue_id),
            op_name='milestoneUpdate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'milestoneUpdate': {
                  'milestone': {
                    'name': 'release-A',
                    'issues': {
                      'edges': [{
                        'node': {
                          'name': 'Issue 1'
                        },
                      }]
                    }
                  }
                }
              }
            }
        )

    def test_remove_all_milestone_issues(self):
        """Test that all issues can be removed from a milestone."""
        milestone = Milestone.objects.create(name='release-A', project=self.project)
        milestone.issues.set(self.issues)
        m_id = base64.b64encode('MilestoneType:{}'.format(
            milestone.id,
        ).encode()).decode()

        r = self.query(
            """
            mutation milestoneUpdate {
              milestoneUpdate (input: {
                id: "%s",
                issues: [],
              }) {
                milestone {
                  name
                  issues {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
            """ % m_id,
            op_name='milestoneUpdate',
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'milestoneUpdate': {
                  'milestone': {
                    'name': 'release-A',
                    'issues': {
                      'edges': []
                    }
                  }
                }
              }
            }
        )
