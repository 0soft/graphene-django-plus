import collections
from typing import TYPE_CHECKING, List, Tuple, Type, TypeVar, Union

try:
    from guardian.core import ObjectPermissionChecker
    from guardian.shortcuts import get_objects_for_user

    has_guardian = True
except ImportError:  # pragma: no cover
    has_guardian = False

from django.apps import apps
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from guardian.core import ObjectPermissionChecker  # noqa: F811

_T = TypeVar("_T", bound="GuardedModel")
_TR = TypeVar("_TR", bound="GuardedRelatedModel")


def _separate_perms(
    perms: collections.Iterable,
    model: Type[models.Model],
) -> Tuple[List[str], List[str]]:
    perms = set(perms)
    own_perms = perms & (
        {p[0] for p in model._meta.permissions}
        | {f"{model._meta.app_label}.{p[0]}" for p in model._meta.permissions}
    )
    other_perms = perms - own_perms
    return list(other_perms), list(own_perms)


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


class GuardedRelatedManager(GuardedModelManager[_TR]):
    """Manager for objects related to companies."""

    model: Type[_TR]

    def for_user(
        self,
        user: Union[AbstractUser, AnonymousUser],
        perms: Union[str, List[str]],
        any_perm: bool = True,
        with_superuser: bool = True,
    ) -> models.QuerySet[_TR]:
        if not user or not user.is_authenticated:
            return self.none()

        other_perms, own_perms = _separate_perms(perms, self.model)

        if own_perms:
            own_qs = super().for_user(
                user,
                own_perms,
                any_perm=any_perm,
                with_superuser=with_superuser,
            )
        else:
            own_qs = None

        if other_perms:
            m = self.model.related_model
            if isinstance(m, str):
                app_label, model_name = m.split(".")
                m = apps.get_model(app_label=app_label, model_name=model_name)

            other_qs = self.all().filter(
                **{
                    f"{self.model.related_attr}__in": m.objects.for_user(
                        user,
                        other_perms,
                        any_perm=any_perm,
                        with_superuser=with_superuser,
                    ),
                }
            )
        else:
            other_qs = None

        if own_qs is not None and other_qs is not None:
            if any_perm:
                return own_qs | other_qs
            else:
                return own_qs & other_qs
        elif own_qs is not None:
            return own_qs
        elif other_qs is not None:
            return other_qs
        else:
            raise AssertionError


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


class GuardedRelatedModel(GuardedModel):
    """Base model for objects that are related to other guarded model."""

    class Meta:
        abstract = True

    objects = GuardedRelatedManager["GuardedRelatedModel"]()
    related_model: Union[GuardedModel, str]
    related_attr: str

    def has_perm(
        self,
        user: Union[AbstractUser, AnonymousUser],
        perms: Union[str, List[str]],
        any_perm: bool = False,
        checker: Union[ObjectPermissionChecker, None] = None,
    ) -> bool:
        checker = checker or ObjectPermissionChecker(user)
        other_perms, own_perms = _separate_perms(perms, self.__class__)

        if own_perms:
            own_check = lambda: super().has_perm(
                user,
                list(own_perms),
                any_perm=any_perm,
                checker=checker,
            )
        else:
            own_check = lambda: True

        if other_perms:
            assert self.related_attr is not None
            related = getattr(self, self.related_attr)
            other_check = lambda: related.has_perm(
                user,
                other_perms,
                any_perm=any_perm,
                checker=checker,
            )
        else:
            other_check = lambda: True

        f = any if any_perm else all
        # Using lambdas will short-cut own_check when own_check is True
        # and we are checking for any_perm
        return f(check() for check in [other_check, own_check])
