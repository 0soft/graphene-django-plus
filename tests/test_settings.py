from django.test import TestCase, override_settings

from graphene_django_plus.settings import graphene_django_plus_settings


class TestSettings(TestCase):

    def test_compatibility_with_override_settings(self):
        self.assertTrue(
            graphene_django_plus_settings.MUTATIONS_INCLUDE_REVERSE_RELATIONS
        )

        with override_settings(GRAPHENE_DJANGO_PLUS={'MUTATIONS_INCLUDE_REVERSE_RELATIONS': False}):
            self.assertFalse(
                graphene_django_plus_settings.MUTATIONS_INCLUDE_REVERSE_RELATIONS
            )  # Setting should have been updated

        self.assertTrue(
            graphene_django_plus_settings.MUTATIONS_INCLUDE_REVERSE_RELATIONS
        )  # Setting should have been restored
