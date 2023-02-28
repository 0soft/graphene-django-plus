import base64
import json
from unittest import mock

from graphene_django import DjangoObjectType
from graphql_relay import to_global_id

from .base import BaseTestCase
from .schema import IssueType


class TestTypes(BaseTestCase):
    def test_results(self):
        # projects
        r = self.query(
            """
            query projects {
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
            operation_name="projects",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "projects": {
                        "edges": [
                            {
                                "node": {
                                    "name": "Test Project",
                                    "milestones": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "name": "Milestone 1",
                                                    "issues": {
                                                        "edges": [
                                                            {"node": {"name": "Issue 1"}},
                                                            {"node": {"name": "Issue 2"}},
                                                        ]
                                                    },
                                                }
                                            },
                                            {
                                                "node": {
                                                    "name": "Milestone 2",
                                                    "issues": {"edges": []},
                                                }
                                            },
                                        ]
                                    },
                                }
                            }
                        ]
                    }
                }
            },
        )

        # issues
        r = self.query(
            """
            query issues {
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
            operation_name="issues",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "issues": {
                        "edges": [
                            {
                                "node": {
                                    "name": "Issue 1",
                                    "milestone": {
                                        "name": "Milestone 1",
                                        "project": {"name": "Test Project"},
                                    },
                                }
                            },
                            {
                                "node": {
                                    "name": "Issue 2",
                                    "milestone": {
                                        "name": "Milestone 1",
                                        "project": {"name": "Test Project"},
                                    },
                                }
                            },
                        ]
                    }
                }
            },
        )

    @mock.patch("graphene_django_plus.types.gql_optimizer", None)
    def test_results_no_gql_optimizer(self):
        # projects
        r = self.query(
            """
            query projects {
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
            operation_name="projects",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "projects": {
                        "edges": [
                            {
                                "node": {
                                    "name": "Test Project",
                                    "milestones": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "name": "Milestone 1",
                                                    "issues": {
                                                        "edges": [
                                                            {"node": {"name": "Issue 1"}},
                                                            {"node": {"name": "Issue 2"}},
                                                        ]
                                                    },
                                                }
                                            },
                                            {
                                                "node": {
                                                    "name": "Milestone 2",
                                                    "issues": {"edges": []},
                                                }
                                            },
                                        ]
                                    },
                                }
                            }
                        ]
                    }
                }
            },
        )

        # issues
        r = self.query(
            """
            query issues {
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
            operation_name="issues",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "issues": {
                        "edges": [
                            {
                                "node": {
                                    "name": "Issue 1",
                                    "milestone": {
                                        "name": "Milestone 1",
                                        "project": {"name": "Test Project"},
                                    },
                                }
                            },
                            {
                                "node": {
                                    "name": "Issue 2",
                                    "milestone": {
                                        "name": "Milestone 1",
                                        "project": {"name": "Test Project"},
                                    },
                                }
                            },
                        ]
                    }
                }
            },
        )

    def test_result(self):
        # project
        p_id = base64.b64encode(
            "ProjectType:{}".format(
                self.project.id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query project {
              project (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
            operation_name="project",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"project": {"name": "Test Project"}}},
        )

        # issue (allowed)
        p_id = base64.b64encode(
            "IssueType:{}".format(
                self.allowed_issues[0].id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query issue {
              issue (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
            operation_name="issue",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"issue": {"name": "Issue 1"}}},
        )

        # issue with more data (allowed)
        p_id = base64.b64encode(
            "IssueType:{}".format(
                self.allowed_issues[0].id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query issue {
              issue (id: "%s") {
                name
                milestone {
                  name
                  project {
                    name
                  }
                }
              }
            }
            """
            % (p_id,),
            operation_name="issue",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "issue": {
                        "name": "Issue 1",
                        "milestone": {
                            "name": "Milestone 1",
                            "project": {
                                "name": "Test Project",
                            },
                        },
                    }
                }
            },
        )

        # issue (not allowed)
        p_id = base64.b64encode(
            "IssueType:{}".format(
                self.unallowed_issues[0].id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query issue {
              issue (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
            operation_name="issue",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"issue": None}},
        )

    @mock.patch("graphene_django_plus.types.gql_optimizer", None)
    def test_result_no_gql_optimizer(self):
        # project
        p_id = base64.b64encode(
            "ProjectType:{}".format(
                self.project.id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query project {
              project (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
            operation_name="project",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"project": {"name": "Test Project"}}},
        )

        # issue (allowed)
        p_id = base64.b64encode(
            "IssueType:{}".format(
                self.allowed_issues[0].id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query issue {
              issue (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
            operation_name="issue",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"issue": {"name": "Issue 1"}}},
        )

        # issue with more data (allowed)
        p_id = base64.b64encode(
            "IssueType:{}".format(
                self.allowed_issues[0].id,
            ).encode()
        ).decode()
        r = self.query(
            """
            query issue {
              issue (id: "%s") {
                name
                milestone {
                  name
                  project {
                    name
                  }
                }
              }
            }
            """
            % (p_id,),
            operation_name="issue",
        )
        self.assertEqual(
            json.loads(r.content),
            {
                "data": {
                    "issue": {
                        "name": "Issue 1",
                        "milestone": {
                            "name": "Milestone 1",
                            "project": {
                                "name": "Test Project",
                            },
                        },
                    }
                }
            },
        )

        with mock.patch.object(
            IssueType,
            "get_node",
            lambda info, id: DjangoObjectType.get_node.__func__(IssueType, info, id),
        ):
            # issue (not allowed)
            p_id = base64.b64encode(
                "IssueType:{}".format(
                    self.unallowed_issues[0].id,
                ).encode()
            ).decode()
            r = self.query(
                """
                query issue {
                  issue (id: "%s") {
                    name
                  }
                }
                """
                % (p_id,),
                operation_name="issue",
            )
            self.assertEqual(
                json.loads(r.content),
                {"data": {"issue": None}},
            )

    def test_result_non_global_registry(self):
        """Test that query using non global registry is working and using correct model type."""
        # project
        p_id = to_global_id("ProjectNameOnlyType", self.project.id)
        r = self.query(
            """
            query project {
              projectNameOnly (id: "%s") {
                name
              }
            }
            """
            % (p_id,),
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"projectNameOnly": {"name": "Test Project"}}},
        )

        r = self.query(
            """
            query project {
              projectNameOnly (id: "%s") {
                cost
              }
            }
            """
            % (p_id,),
        )
        self.assertEqual(
            json.loads(r.content)["errors"][0]["message"],
            "Cannot query field 'cost' on type 'ProjectNameOnlyType'.",
        )
