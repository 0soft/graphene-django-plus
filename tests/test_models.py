from unittest import mock

from .base import BaseTestCase
from .models import Issue


class TestModels(BaseTestCase):

    def test_for_user(self):
        self.assertEqual(
            set(Issue.objects.for_user(self.user, ['can_read'])),
            set(self.allowed_issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(self.user, 'can_read')),
            set(self.allowed_issues),
        )

    def test_has_perm(self):
        for i in self.issues:
            if i in self.allowed_issues:
                self.assertTrue(i.has_perm(self.user, ['can_read']))
                self.assertTrue(i.has_perm(self.user, 'can_read'))
            else:
                self.assertFalse(i.has_perm(self.user, ['can_read']))
                self.assertFalse(i.has_perm(self.user, 'can_read'))

    @mock.patch('graphene_django_plus.models.has_guardian', False)
    def test_for_user_no_guardian(self):
        self.assertEqual(
            set(Issue.objects.for_user(self.user, ['can_read'])),
            set(self.issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(self.user, 'can_read')),
            set(self.issues),
        )

    @mock.patch('graphene_django_plus.models.has_guardian', False)
    def test_has_perm_no_guardian(self):
        for i in self.issues:
            self.assertTrue(i.has_perm(self.user, ['can_read']))
            self.assertTrue(i.has_perm(self.user, 'can_read'))
