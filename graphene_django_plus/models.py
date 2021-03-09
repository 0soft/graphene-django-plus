try:
    from guardian.core import ObjectPermissionChecker
    from guardian.shortcuts import get_objects_for_user

    has_guardian = True
except ImportError:  # pragma: no cover
    has_guardian = False

from django.db import models


class GuardedModelManager(models.Manager):
    """Model manager that integrates with guardian to check for permissions."""

    def for_user(self, user, perms, any_perm=False, with_superuser=False):
        """Get a queryset filtered by perms for the user.

        :param user: the user itself
        :param perms: a string or list of perms to check for
        :param any_perm: if any perm or all perms should be cosidered
        :param with_superuser: if a superuser should skip the checks
        """
        if not has_guardian:
            return self.all()

        perms = [perms] if isinstance(perms, str) else perms

        return get_objects_for_user(
            user,
            perms,
            klass=self.model,
            any_perm=any_perm,
            with_superuser=with_superuser,
        )


class GuardedModel(models.Model):
    """Model that integrates with guardian to check for permissions."""

    class Meta:
        abstract = True

    objects = GuardedModelManager()

    def has_perm(self, user, perms, any_perm=False, checker=None):
        """Check if the user has the given permissions to this object.

        :param user: the user itself
        :param perms: a string or list of perms to check for
        :param any_perm: if any perm or all perms should be cosidered
        :param checker: a `guardian.core.ObjectPermissionChecker` that
            can be used to optimize performance in checking for permissions
        """
        if not has_guardian:
            return True

        checker = checker or ObjectPermissionChecker(user)
        perms = [perms] if isinstance(perms, str) else perms

        f = any if any_perm else all
        return f(checker.has_perm(p, self) for p in perms)
