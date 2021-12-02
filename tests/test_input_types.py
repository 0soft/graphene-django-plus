import graphene
from django.db import models
from graphene_django.registry import get_global_registry

from graphene_django_plus.input_types import get_input_field
from .base import BaseTestCase
from .models import Project

_registry = get_global_registry()


class TestInputTypes(BaseTestCase):
    def test_char(self):
        field = models.CharField()
        input_field = get_input_field(field, _registry)
        self.assertEqual(input_field._meta.name, "String")

    def test_boolean(self):
        field = models.BooleanField()
        input_field = get_input_field(field, _registry)
        self.assertEqual(input_field._meta.name, "Boolean")

    def test_foreign_key(self):
        field = models.ForeignKey(Project, on_delete=models.CASCADE)
        input_field = get_input_field(field, _registry)
        self.assertEqual(input_field._meta.name, "ID")

    def test_one_to_one(self):
        field = models.OneToOneField(Project, on_delete=models.CASCADE)
        input_field = get_input_field(field, _registry)
        self.assertEqual(input_field._meta.name, "ID")

    def test_many_to_many(self):
        field = models.ManyToManyField(Project)
        input_field = get_input_field(field, _registry)
        self.assertTrue(isinstance(input_field, graphene.List))
        self.assertEqual(input_field.of_type._meta.name, "ID")

    def test_many_to_one_relation(self):
        field = models.ManyToOneRel(
            models.ForeignKey(Project, on_delete=models.CASCADE), Project, "projects"
        )
        setattr(
            field, "related_model", Project
        )  # set this manually because django does not initialize the model
        input_field = get_input_field(field, _registry)
        self.assertTrue(isinstance(input_field, graphene.List))
        self.assertEqual(input_field.of_type._meta.name, "ID")

    def test_many_to_many_relation(self):
        field = models.ManyToManyRel(
            models.ForeignKey(Project, on_delete=models.CASCADE), Project, "projects"
        )
        setattr(
            field, "related_model", Project
        )  # set this manually because django does not initialize the model
        input_field = get_input_field(field, _registry)
        self.assertTrue(isinstance(input_field, graphene.List))
        self.assertEqual(input_field.of_type._meta.name, "ID")
