from typing import TYPE_CHECKING, List, TypeVar, Union

try:
    from guardian.core import ObjectPermissionChecker
    from guardian.shortcuts import get_objects_for_user

    has_guardian = True
except ImportError:  # pragma: no cover
    has_guardian = False

from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from guardian.core import ObjectPermissionChecker  # noqa: F811

_T = TypeVar("_T", bound=models.Model, covariant=True)


class GuardedModelManager(models.Manager[_T]):
    """Model manager that integrates with guardian to check for permissions."""

    def for_user(
        self,
        user: Union[AbstractUser, AnonymousUser],
        perms: Union[str, List[str]],
        any_perm: bool = False,
        with_superuser: bool = True,
    ) -> QuerySet[_T]:
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

    # NOTE: This should be adjusted in each model using this class
    # for better typing support
    objects = GuardedModelManager["GuardedModel"]()

    def has_perm(
        self,
        user: Union[AbstractUser, AnonymousUser],
        perms: Union[str, List[str]],
        any_perm: bool = False,
        checker: Union[ObjectPermissionChecker, None] = None,
    ) -> bool:
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

        # First try to check if the user has global permissions for this
        # Otherwise we will check for the objeect itself bellow
        if f(user.has_perm(p) for p in perms):
            return True

        return f(checker.has_perm(p, self) for p in perms)
