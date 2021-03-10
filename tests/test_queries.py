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
                  field
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  verboseName
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
                        "field": "name",
                        "helpText": "",
                        "kind": "STRING",
                        "maxDigits": None,
                        "maxLength": 255,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "verboseName": "name",
                    },
                    {
                        "choices": [
                            {"label": "Bug", "name": "B", "value": '"b"'},
                            {"label": "Feature", "name": "F", "value": '"f"'},
                        ],
                        "decimalPlaces": None,
                        "field": "kind",
                        "helpText": "the kind of the issue",
                        "kind": "STRING",
                        "maxDigits": None,
                        "maxLength": 1,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "verboseName": "kind",
                    },
                    {
                        "choices": None,
                        "decimalPlaces": None,
                        "field": "priority",
                        "helpText": "",
                        "kind": "INTEGER",
                        "maxDigits": None,
                        "maxLength": None,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": None,
                        "verboseName": "priority",
                    },
                    {
                        "choices": None,
                        "decimalPlaces": None,
                        "field": "milestone",
                        "helpText": "",
                        "kind": "ID",
                        "maxDigits": None,
                        "maxLength": None,
                        "maxValue": None,
                        "minLength": None,
                        "minValue": None,
                        "multiple": "false",
                        "ofType": "MilestoneType",
                        "verboseName": "milestone",
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
                  field
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  verboseName
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
                  field
                  kind
                  multiple
                  choices {
                    label
                    name
                    value
                  }
                  verboseName
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
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "decimalPlaces": None,
                            "field": "kind",
                            "helpText": "the kind of the issue",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 1,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "kind",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "priority",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "priority",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "milestone",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "MilestoneType",
                            "verboseName": "milestone",
                        },
                    ],
                    "inputObject": "IssueCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        }
                    ],
                    "inputObject": "IssueDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "decimalPlaces": None,
                            "field": "kind",
                            "helpText": "the kind of the issue",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 1,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "kind",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "priority",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "priority",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "milestone",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "MilestoneType",
                            "verboseName": "milestone",
                        },
                    ],
                    "inputObject": "IssueUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "due date",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "project",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "ProjectType",
                            "verboseName": "project",
                        },
                    ],
                    "inputObject": "MilestoneCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        }
                    ],
                    "inputObject": "MilestoneDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "due date",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "project",
                            "helpText": "",
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": "ProjectType",
                            "verboseName": "project",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "issues",
                            "helpText": None,
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "true",
                            "ofType": "IssueType",
                            "verboseName": None,
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "milestonecomment_set",
                            "helpText": None,
                            "kind": "ID",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "true",
                            "ofType": "MilestoneCommentType",
                            "verboseName": None,
                        },
                    ],
                    "inputObject": "MilestoneUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "due date",
                        },
                    ],
                    "inputObject": "ProjectCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        }
                    ],
                    "inputObject": "ProjectDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "id",
                            "helpText": "",
                            "kind": "INTEGER",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "ID",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "name",
                            "helpText": "",
                            "kind": "STRING",
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "name",
                        },
                        {
                            "choices": None,
                            "decimalPlaces": None,
                            "field": "due_date",
                            "helpText": "",
                            "kind": "DATE",
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "multiple": "false",
                            "ofType": None,
                            "verboseName": "due date",
                        },
                    ],
                    "inputObject": "ProjectUpdateMutationInput",
                },
            ],
        )
