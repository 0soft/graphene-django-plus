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

    def test_results(self):
        # projects
        r = self.query(
            """
            query {
              projects {
                edges {
                  node {
                    name
                    milestones {
                      edges {
                        node {
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
                  }
                }
              }
            }
            """,
            op_name='projects'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'projects': {
                    'edges': [
                        {'node': {
                            'name': 'Test Project',
                            'milestones': {
                                'edges': [
                                    {'node': {
                                        'name': 'Milestone 1',
                                        'issues': {
                                            'edges': [
                                                {'node': {
                                                    'name': 'Issue 1'
                                                }},
                                                {'node': {
                                                    'name': 'Issue 2'
                                                }}
                                            ]
                                        }
                                    }},
                                    {'node': {
                                        'name': 'Milestone 2',
                                        'issues': {
                                            'edges': []
                                        }
                                    }}
                                ]
                            }
                        }}
                    ]
                }
            }}
        )

        # issues
        r = self.query(
            """
            query {
              issues {
                edges {
                  node {
                    name
                    milestone {
                      name
                      project {
                        name
                      }
                    }
                  }
                }
              }
            }
            """,
            op_name='issues'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'issues': {
                    'edges': [
                        {'node': {
                            'name': 'Issue 1',
                            'milestone': {
                                'name': 'Milestone 1',
                                'project': {
                                    'name': 'Test Project'
                                }
                            }
                        }},
                        {'node': {
                            'name': 'Issue 2',
                            'milestone': {
                                'name': 'Milestone 1',
                                'project': {
                                    'name': 'Test Project'
                                }
                            }
                        }}
                    ]
                }
            }}
        )

    @mock.patch('graphene_django_plus.types.gql_optimizer', None)
    def test_results_no_gql_optimizer(self):
        # projects
        r = self.query(
            """
            query {
              projects {
                edges {
                  node {
                    name
                    milestones {
                      edges {
                        node {
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
                  }
                }
              }
            }
            """,
            op_name='projects'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'projects': {
                    'edges': [
                        {'node': {
                            'name': 'Test Project',
                            'milestones': {
                                'edges': [
                                    {'node': {
                                        'name': 'Milestone 1',
                                        'issues': {
                                            'edges': [
                                                {'node': {
                                                    'name': 'Issue 1'
                                                }},
                                                {'node': {
                                                    'name': 'Issue 2'
                                                }}
                                            ]
                                        }
                                    }},
                                    {'node': {
                                        'name': 'Milestone 2',
                                        'issues': {
                                            'edges': []
                                        }
                                    }}
                                ]
                            }
                        }}
                    ]
                }
            }}
        )

        # issues
        r = self.query(
            """
            query {
              issues {
                edges {
                  node {
                    name
                    milestone {
                      name
                      project {
                        name
                      }
                    }
                  }
                }
              }
            }
            """,
            op_name='issues'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {
                'issues': {
                    'edges': [
                        {'node': {
                            'name': 'Issue 1',
                            'milestone': {
                                'name': 'Milestone 1',
                                'project': {
                                    'name': 'Test Project'
                                }
                            }
                        }},
                        {'node': {
                            'name': 'Issue 2',
                            'milestone': {
                                'name': 'Milestone 1',
                                'project': {
                                    'name': 'Test Project'
                                }
                            }
                        }}
                    ]
                }
            }}
        )

    def test_result(self):
        # project
        p_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              project (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='project'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'project': {'name': 'Test Project'}}},
        )

        # issue (allowed)
        p_id = base64.b64encode('IssueType:{}'.format(
            self.allowed_issues[0].id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              issue (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='issue'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'issue': {'name': 'Issue 1'}}},
        )

        # issue (not allowed)
        p_id = base64.b64encode('IssueType:{}'.format(
            self.unallowed_issues[0].id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              issue (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='issue'
        )
        self.assertResponseHasErrors(r)

    @mock.patch('graphene_django_plus.types.gql_optimizer', None)
    def test_result_no_gql_optimizer(self):
        # project
        p_id = base64.b64encode('ProjectType:{}'.format(
            self.project.id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              project (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='project'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'project': {'name': 'Test Project'}}},
        )

        # issue (allowed)
        p_id = base64.b64encode('IssueType:{}'.format(
            self.allowed_issues[0].id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              issue (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='issue'
        )
        self.assertEqual(
            json.loads(r.content),
            {'data': {'issue': {'name': 'Issue 1'}}},
        )

        # issue (not allowed)
        p_id = base64.b64encode('IssueType:{}'.format(
            self.unallowed_issues[0].id,
        ).encode()).decode()
        r = self.query(
            """
            query {
              issue (id: "%s") {
                name
              }
            }
            """ % (p_id, ),
            op_name='issue'
        )
        self.assertResponseHasErrors(r)
