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
                  hidden
                  label
                  helpText
                  defaultValue
                  ofType
                  validation {
                    required
                    minLength
                    maxLength
                    minValue
                    maxValue
                    maxDigits
                    decimalPlaces
                  }
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
                        "defaultValue": None,
                        "helpText": "",
                        "hidden": False,
                        "kind": "STRING",
                        "label": "name",
                        "multiple": False,
                        "name": "name",
                        "ofType": None,
                        "validation": {
                            "decimalPlaces": None,
                            "maxDigits": None,
                            "maxLength": 255,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "required": True,
                        },
                    },
                    {
                        "choices": [
                            {"label": "Bug", "name": "B", "value": '"b"'},
                            {"label": "Feature", "name": "F", "value": '"f"'},
                        ],
                        "defaultValue": None,
                        "helpText": "the kind of the issue",
                        "hidden": False,
                        "kind": "STRING",
                        "label": "kind",
                        "multiple": False,
                        "name": "kind",
                        "ofType": None,
                        "validation": {
                            "decimalPlaces": None,
                            "maxDigits": None,
                            "maxLength": 1,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "required": False,
                        },
                    },
                    {
                        "choices": None,
                        "defaultValue": "0",
                        "helpText": "",
                        "hidden": False,
                        "kind": "INTEGER",
                        "label": "priority",
                        "multiple": False,
                        "name": "priority",
                        "ofType": None,
                        "validation": {
                            "decimalPlaces": None,
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "required": False,
                        },
                    },
                    {
                        "choices": None,
                        "defaultValue": None,
                        "helpText": "",
                        "hidden": False,
                        "kind": "ID",
                        "label": "milestone",
                        "multiple": False,
                        "name": "milestone",
                        "ofType": "MilestoneType",
                        "validation": {
                            "decimalPlaces": None,
                            "maxDigits": None,
                            "maxLength": None,
                            "maxValue": None,
                            "minLength": None,
                            "minValue": None,
                            "required": False,
                        },
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
                  hidden
                  label
                  helpText
                  defaultValue
                  ofType
                  validation {
                    required
                    minLength
                    maxLength
                    minValue
                    maxValue
                    maxDigits
                    decimalPlaces
                  }
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
                  hidden
                  label
                  helpText
                  defaultValue
                  ofType
                  validation {
                    required
                    minLength
                    maxLength
                    minValue
                    maxValue
                    maxDigits
                    decimalPlaces
                  }
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
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "defaultValue": None,
                            "helpText": "the kind of the issue",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "kind",
                            "multiple": False,
                            "name": "kind",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 1,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": "0",
                            "helpText": "",
                            "hidden": False,
                            "kind": "INTEGER",
                            "label": "priority",
                            "multiple": False,
                            "name": "priority",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "ID",
                            "label": "milestone",
                            "multiple": False,
                            "name": "milestone",
                            "ofType": "MilestoneType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                    ],
                    "inputObject": "IssueCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        }
                    ],
                    "inputObject": "IssueDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "defaultValue": None,
                            "helpText": "the kind of the issue",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "kind",
                            "multiple": False,
                            "name": "kind",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 1,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": "0",
                            "helpText": "",
                            "hidden": False,
                            "kind": "INTEGER",
                            "label": "priority",
                            "multiple": False,
                            "name": "priority",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "ID",
                            "label": "milestone",
                            "multiple": False,
                            "name": "milestone",
                            "ofType": "MilestoneType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                    ],
                    "inputObject": "IssueUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "DATE",
                            "label": "due date",
                            "multiple": False,
                            "name": "dueDate",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "ID",
                            "label": "project",
                            "multiple": False,
                            "name": "project",
                            "ofType": "ProjectType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                    ],
                    "inputObject": "MilestoneCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        }
                    ],
                    "inputObject": "MilestoneDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "DATE",
                            "label": "due date",
                            "multiple": False,
                            "name": "dueDate",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "ID",
                            "label": "project",
                            "multiple": False,
                            "name": "project",
                            "ofType": "ProjectType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": None,
                            "hidden": False,
                            "kind": "ID",
                            "label": None,
                            "multiple": True,
                            "name": "issues",
                            "ofType": "IssueType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": None,
                            "hidden": False,
                            "kind": "ID",
                            "label": None,
                            "multiple": True,
                            "name": "milestonecommentSet",
                            "ofType": "MilestoneCommentType",
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                    ],
                    "inputObject": "MilestoneUpdateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "DATE",
                            "label": "due date",
                            "multiple": False,
                            "name": "dueDate",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                    ],
                    "inputObject": "ProjectCreateMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        }
                    ],
                    "inputObject": "ProjectDeleteMutationInput",
                },
                {
                    "fields": [
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": True,
                            "kind": "INTEGER",
                            "label": "ID",
                            "multiple": False,
                            "name": "id",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": True,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "STRING",
                            "label": "name",
                            "multiple": False,
                            "name": "name",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": 255,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                        {
                            "choices": None,
                            "defaultValue": None,
                            "helpText": "",
                            "hidden": False,
                            "kind": "DATE",
                            "label": "due date",
                            "multiple": False,
                            "name": "dueDate",
                            "ofType": None,
                            "validation": {
                                "decimalPlaces": None,
                                "maxDigits": None,
                                "maxLength": None,
                                "maxValue": None,
                                "minLength": None,
                                "minValue": None,
                                "required": False,
                            },
                        },
                    ],
                    "inputObject": "ProjectUpdateMutationInput",
                },
            ],
        )
