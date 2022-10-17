import json
from unittest import mock

from .base import BaseTestCase


class TestModels(BaseTestCase):
    def test_orderby(self):
        # milestones
        r = self.query(
            """
            query milestones {
                milestones (orderby: ["name"]) {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
            """,
            operation_name="milestones",
        )
        d = (json.loads(r.content),)
        edges = d[0]["data"]["milestones"]["edges"]
        self.assertEqual(
            edges[0]["node"]["name"],
            "Milestone 1",
        )
        self.assertEqual(
            edges[1]["node"]["name"],
            "Milestone 2",
        )

        # milestones reversed
        r = self.query(
            """
            query milestones {
                milestones (orderby: ["-name"]) {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
            """,
            operation_name="milestones",
        )
        d = (json.loads(r.content),)
        edges = d[0]["data"]["milestones"]["edges"]
        self.assertEqual(
            edges[0]["node"]["name"],
            "Milestone 2",
        )
        self.assertEqual(
            edges[1]["node"]["name"],
            "Milestone 1",
        )

    def test_total_count(self):
        # projects
        r = self.query(
            """
            query projects {
                projects {
                    totalCount
                }
            }
            """,
            operation_name="projects",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"projects": {"totalCount": 1}}},
        )

        # milestones
        r = self.query(
            """
            query milestones {
                milestones {
                    totalCount
                }
            }
            """,
            operation_name="milestones",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"milestones": {"totalCount": 2}}},
        )

        # issues
        r = self.query(
            """
            query issues {
                issues {
                    totalCount
                }
            }
            """,
            operation_name="issues",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"issues": {"totalCount": 2}}},
        )

    @mock.patch("graphene_django_plus.types.gql_optimizer", None)
    def test_total_count_no_gql_optimizer(self):
        # projects
        r = self.query(
            """
            query projects {
                projects {
                    totalCount
                }
            }
            """,
            operation_name="projects",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"projects": {"totalCount": 1}}},
        )

        # milestones
        r = self.query(
            """
            query milestones {
                milestones {
                    totalCount
                }
            }
            """,
            operation_name="milestones",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"milestones": {"totalCount": 2}}},
        )

        # issues
        r = self.query(
            """
            query issues {
                issues {
                    totalCount
                }
            }
            """,
            operation_name="issues",
        )
        self.assertEqual(
            json.loads(r.content),
            {"data": {"issues": {"totalCount": 2}}},
        )
