import json

from .base import BaseTestCase


class TestQueries(BaseTestCase):
    def test_gql_input_schema(self):
        r = self.query(
            """
            query inputschema {
              gqlInputSchema (inputObject: "IssueCreateMutationInput") {
                inputObject
                fields {
                  name
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  label
                  helpText
                  minLength
                  maxLength
                  minValue
                  maxValue
                  maxDigits
                  decimalPlaces
                  ofType
                }
              }
            }
            """,
            op_name="inputschema",
        )
        d = json.loads(r.content)
        self.assertEqual(
            d["data"]["gqlInputSchema"],
            {
                "fields": [
                    {
                        "choices": None,
                        "decimalPlaces": None,
                        "name": "name",
                        "helpText": "",
                        "kind": "STRING",
                        "maxDigits": None,
                        "maxLength": 255,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "label": "name",
                    },
                    {
                        "choices": [
                            {"label": "Bug", "name": "B", "value": '"b"'},
                            {"label": "Feature", "name": "F", "value": '"f"'},
                        ],
                        "decimalPlaces": None,
                        "name": "kind",
                        "helpText": "the kind of the issue",
                        "kind": "STRING",
                        "maxDigits": None,
                        "maxLength": 1,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "label": "kind",
                    },
                    {
                        "choices": None,
                        "decimalPlaces": None,
                        "name": "priority",
                        "helpText": "",
                        "kind": "INTEGER",
                        "maxDigits": None,
                        "maxLength": None,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "label": "priority",
                    },
                    {
                        "choices": None,
                        "decimalPlaces": None,
                        "name": "milestone",
                        "helpText": "",
                        "kind": "ID",
                        "maxDigits": None,
                        "maxLength": None,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": "MilestoneType",
                        "label": "milestone",
                    },
                ],
                "inputObject": "IssueCreateMutationInput",
            },
        )

    def test_gql_input_schema_non_existing(self):
        r = self.query(
            """
            query inputschema {
              gqlInputSchema (inputObject: "NonExisting") {
                inputObject
                fields {
                  name
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  label
                  helpText
                  minLength
                  maxLength
                  minValue
                  maxValue
                  maxDigits
                  decimalPlaces
                  ofType
                }
              }
            }
            """,
            op_name="inputschema",
        )
        d = json.loads(r.content)
        self.assertEqual(d, {"data": {"gqlInputSchema": None}})

    def test_gql_input_schema_all(self):
        r = self.query(
            """
            query inputschema {
              gqlInputSchemaAll {
                inputObject
                fields {
                  name
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  label
                  helpText
                  minLength
                  maxLength
                  minValue
                  maxValue
                  maxDigits
                  decimalPlaces
                  ofType
                }
              }
            }
            """,
            op_name="inputschema",
        )
        d = json.loads(r.content)
        self.assertEqual(
            d["data"]["gqlInputSchemaAll"],
            [
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "decimalPlaces": None,
                            "name": "kind",
                            "helpText": "the kind of the issue",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 1,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "kind",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "priority",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "priority",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "milestone",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "MilestoneType",
                            "label": "milestone",
                        },
                    ],
                    "inputObject": "IssueCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        }
                    ],
                    "inputObject": "IssueDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "decimalPlaces": None,
                            "name": "kind",
                            "helpText": "the kind of the issue",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 1,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "kind",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "priority",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "priority",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "milestone",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "MilestoneType",
                            "label": "milestone",
                        },
                    ],
                    "inputObject": "IssueUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "due date",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "project",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "ProjectType",
                            "label": "project",
                        },
                    ],
                    "inputObject": "MilestoneCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        }
                    ],
                    "inputObject": "MilestoneDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "due date",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "project",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "ProjectType",
                            "label": "project",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "issues",
                            "helpText": None,
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "true",
                            "ofType": "IssueType",
                            "label": None,
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "milestonecomment_set",
                            "helpText": None,
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "true",
                            "ofType": "MilestoneCommentType",
                            "label": None,
                        },
                    ],
                    "inputObject": "MilestoneUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "due date",
                        },
                    ],
                    "inputObject": "ProjectCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        }
                    ],
                    "inputObject": "ProjectDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "name": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "label": "due date",
                        },
                    ],
                    "inputObject": "ProjectUpdateMutationInput",
                },
            ],
        )
