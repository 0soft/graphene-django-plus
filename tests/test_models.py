from unittest import mock

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

from .base import BaseTestCase
from .models import Issue, IssueComment


class TestGuardedModel(BaseTestCase):
    def test_for_user(self):
        self.assertEqual(
            set(Issue.objects.for_user(self.user, ["can_read"])),
            set(self.allowed_issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(self.user, "can_read")),
            set(self.allowed_issues),
        )

    def test_for_user_no_perms(self):
        user = User.objects.create(username="no_perm")
        self.assertEqual(
            set(Issue.objects.for_user(user, ["tests.can_read"])),
            set(),
        )
        self.assertEqual(
            set(Issue.objects.for_user(user, "tests.can_read")),
            set(),
        )

    def test_for_user_global_perm(self):
        user = User.objects.create(username="global_perm")
        ct = ContentType.objects.get_for_model(Issue)
        permission = Permission.objects.get(content_type=ct, codename="can_read")
        user.user_permissions.add(permission)
        self.assertEqual(
            set(Issue.objects.for_user(user, ["tests.can_read"])),
            set(self.issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(user, "tests.can_read")),
            set(self.issues),
        )

    def test_for_user_superuser(self):
        user = User(username="superuser")
        user.is_superuser = True
        user.save()

        self.assertEqual(
            set(Issue.objects.for_user(user, ["can_read"], with_superuser=False)),
            set(),
        )
        self.assertEqual(
            set(Issue.objects.for_user(user, "can_read", with_superuser=False)),
            set(),
        )
        self.assertEqual(
            set(Issue.objects.for_user(user, ["can_read"])),
            set(self.issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(user, "can_read")),
            set(self.issues),
        )

    def test_has_perm_no_perm(self):
        user = User.objects.create(username="no_perm")

        for i in self.issues:
            self.assertFalse(i.has_perm(user, ["can_read"]))
            self.assertFalse(i.has_perm(user, "can_read"))

    def test_has_perm_global_perm(self):
        user = User.objects.create(username="global_perm")
        ct = ContentType.objects.get_for_model(Issue)
        permission = Permission.objects.get(content_type=ct, codename="can_read")
        user.user_permissions.add(permission)

        for i in self.issues:
            self.assertTrue(i.has_perm(user, ["tests.can_read"]))
            self.assertTrue(i.has_perm(user, "tests.can_read"))

    def test_has_perm(self):
        for i in self.issues:
            if i in self.allowed_issues:
                self.assertTrue(i.has_perm(self.user, ["can_read"]))
                self.assertTrue(i.has_perm(self.user, "can_read"))
            else:
                self.assertFalse(i.has_perm(self.user, ["can_read"]))
                self.assertFalse(i.has_perm(self.user, "can_read"))

    def test_has_perm_superuser(self):
        user = User(username="superuser")
        user.is_superuser = True
        user.save()

        for i in self.issues:
            self.assertTrue(i.has_perm(user, ["can_read"]))
            self.assertTrue(i.has_perm(user, "can_read"))

    @mock.patch("graphene_django_plus.models.has_guardian", False)
    def test_for_user_no_guardian(self):
        self.assertEqual(
            set(Issue.objects.for_user(self.user, ["can_read"])),
            set(self.issues),
        )
        self.assertEqual(
            set(Issue.objects.for_user(self.user, "can_read")),
            set(self.issues),
        )

    @mock.patch("graphene_django_plus.models.has_guardian", False)
    def test_has_perm_no_guardian(self):
        for i in self.issues:
            self.assertTrue(i.has_perm(self.user, ["can_read"]))
            self.assertTrue(i.has_perm(self.user, "can_read"))


class TestGuardedRelatedModel(BaseTestCase):
    def test_for_user(self):
        self.assertEqual(
            set(IssueComment.objects.for_user(self.user, ["tests.can_read"])),
            set(self.allowed_issues_comments),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(self.user, "tests.can_read")),
            set(self.allowed_issues_comments),
        )

    def test_for_user_no_perms(self):
        user = User.objects.create(username="no_perm")
        self.assertEqual(
            set(IssueComment.objects.for_user(user, ["tests.can_read"])),
            set(),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(user, "tests.can_read")),
            set(),
        )

    def test_for_user_global_perm(self):
        user = User.objects.create(username="global_perm")
        ct = ContentType.objects.get_for_model(Issue)
        permission = Permission.objects.get(content_type=ct, codename="can_read")
        user.user_permissions.add(permission)
        self.assertEqual(
            set(IssueComment.objects.for_user(user, ["tests.can_read"])),
            set(self.issues_comments),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(user, "tests.can_read")),
            set(self.issues_comments),
        )

    def test_for_user_superuser(self):
        user = User(username="superuser")
        user.is_superuser = True
        user.save()

        self.assertEqual(
            set(IssueComment.objects.for_user(user, ["tests.can_read"], with_superuser=False)),
            set(),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(user, "tests.can_read", with_superuser=False)),
            set(),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(user, ["tests.can_read"])),
            set(self.issues_comments),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(user, "tests.can_read")),
            set(self.issues_comments),
        )

    def test_has_perm_no_perm(self):
        user = User.objects.create(username="no_perm")

        for i in self.issues_comments:
            self.assertFalse(i.has_perm(user, ["tests.can_read"]))
            self.assertFalse(i.has_perm(user, "tests.can_read"))

    def test_has_perm_global_perm(self):
        user = User.objects.create(username="global_perm")
        ct = ContentType.objects.get_for_model(Issue)
        permission = Permission.objects.get(content_type=ct, codename="can_read")
        user.user_permissions.add(permission)

        for i in self.issues_comments:
            self.assertTrue(i.has_perm(user, ["tests.can_read"]))
            self.assertTrue(i.has_perm(user, "tests.can_read"))

    def test_has_perm(self):
        for i in self.issues_comments:
            if i in self.allowed_issues_comments:
                self.assertTrue(i.has_perm(self.user, ["tests.can_read"]))
                self.assertTrue(i.has_perm(self.user, "tests.can_read"))
            else:
                self.assertFalse(i.has_perm(self.user, ["tests.can_read"]))
                self.assertFalse(i.has_perm(self.user, "tests.can_read"))

    def test_has_perm_superuser(self):
        user = User(username="superuser")
        user.is_superuser = True
        user.save()

        for i in self.issues_comments:
            self.assertTrue(i.has_perm(user, ["tests.can_read"]))
            self.assertTrue(i.has_perm(user, "tests.can_read"))

    @mock.patch("graphene_django_plus.models.has_guardian", False)
    def test_for_user_no_guardian(self):
        self.assertEqual(
            set(IssueComment.objects.for_user(self.user, ["tests.can_read"])),
            set(self.issues_comments),
        )
        self.assertEqual(
            set(IssueComment.objects.for_user(self.user, "tests.can_read")),
            set(self.issues_comments),
        )

    @mock.patch("graphene_django_plus.models.has_guardian", False)
    def test_has_perm_no_guardian(self):
        for i in self.issues_comments:
            self.assertTrue(i.has_perm(self.user, ["tests.can_read"]))
            self.assertTrue(i.has_perm(self.user, "tests.can_read"))
