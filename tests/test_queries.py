import json

from .base import BaseTestCase


class TestQueries(BaseTestCase):
    def test_gql_object_schema(self):
        r = self.query(
            """
            query objectschema {
              gqlObjectSchema (objectType: "IssueCreateMutationInput") {
                objectType
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
            op_name="objectschema",
        )
        d = json.loads(r.content)
        self.assertEqual(
            d["data"]["gqlObjectSchema"],
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
                "objectType": "IssueCreateMutationInput",
            },
        )

    def test_gql_object_schema_non_existing(self):
        r = self.query(
            """
            query objectschema {
              gqlObjectSchema (objectType: "NonExisting") {
                objectType
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
            op_name="objectschema",
        )
        d = json.loads(r.content)
        self.assertEqual(d, {"data": {"gqlObjectSchema": None}})

    def test_gql_object_schema_all(self):
        r = self.query(
            """
            query objectschema {
              gqlObjectSchemaAll {
                objectType
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
            op_name="objectschema",
        )
        d = json.loads(r.content)
        self.assertEqual(
            d["data"]["gqlObjectSchemaAll"],
            [
                {
                    "objectType": "IssueCreateMutationInput",
                    "fields": [
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "kind",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "hidden": False,
                            "label": "kind",
                            "helpText": "the kind of the issue",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 1,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "priority",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "priority",
                            "helpText": "",
                            "defaultValue": "0",
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestone",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "milestone",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": "MilestoneType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "IssueDeleteMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        }
                    ],
                },
                {
                    "objectType": "IssueType",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "kind",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "hidden": False,
                            "label": "kind",
                            "helpText": "the kind of the issue",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 1,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "priority",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "priority",
                            "helpText": "",
                            "defaultValue": "0",
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestone",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "milestone",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "IssueUpdateMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "kind",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": [
                                {"label": "Bug", "name": "B", "value": '"b"'},
                                {"label": "Feature", "name": "F", "value": '"f"'},
                            ],
                            "hidden": False,
                            "label": "kind",
                            "helpText": "the kind of the issue",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 1,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "priority",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "priority",
                            "helpText": "",
                            "defaultValue": "0",
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestone",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "milestone",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": "MilestoneType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "MilestoneCommentType",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "text",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "text",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestone",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "milestone",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": "MilestoneType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "MilestoneCreateMutationInput",
                    "fields": [
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "project",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "project",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": "ProjectType",
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "issues",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": "IssueType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestonecommentSet",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": "MilestoneCommentType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "MilestoneDeleteMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        }
                    ],
                },
                {
                    "objectType": "MilestoneType",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "project",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "project",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "issues",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": "IssueType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestonecommentSet",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "MilestoneUpdateMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "project",
                            "kind": "ID",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "project",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": "ProjectType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "issues",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": "IssueType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "milestonecommentSet",
                            "kind": "ID",
                            "multiple": True,
                            "choices": None,
                            "hidden": False,
                            "label": None,
                            "helpText": None,
                            "defaultValue": None,
                            "ofType": "MilestoneCommentType",
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "ProjectCreateMutationInput",
                    "fields": [
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "ProjectDeleteMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        }
                    ],
                },
                {
                    "objectType": "ProjectType",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
                {
                    "objectType": "ProjectUpdateMutationInput",
                    "fields": [
                        {
                            "name": "id",
                            "kind": "INTEGER",
                            "multiple": False,
                            "choices": None,
                            "hidden": True,
                            "label": "ID",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": True,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "name",
                            "kind": "STRING",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "name",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": 255,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                        {
                            "name": "dueDate",
                            "kind": "DATE",
                            "multiple": False,
                            "choices": None,
                            "hidden": False,
                            "label": "due date",
                            "helpText": "",
                            "defaultValue": None,
                            "ofType": None,
                            "validation": {
                                "required": False,
                                "minLength": None,
                                "maxLength": None,
                                "minValue": None,
                                "maxValue": None,
                                "maxDigits": None,
                                "decimalPlaces": None,
                            },
                        },
                    ],
                },
            ],
        )
