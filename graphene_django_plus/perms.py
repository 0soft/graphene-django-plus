from typing import List, Optional, Union

from django.contrib.auth.models import AbstractUser, AnonymousUser

from .exceptions import PermissionDenied


def check_authenticated(user: Union[AbstractUser, AnonymousUser]):
    return user and user.is_authenticated


def assert_authenticated(user: Union[AbstractUser, AnonymousUser], msg: Optional[str] = None):
    if not check_authenticated(user):
        raise PermissionDenied(msg or "You don't have permissions to do this...")


def check_superuser(user: Union[AbstractUser, AnonymousUser]):
    return check_authenticated(user) and user.is_superuser


def assert_superuser(user: Union[AbstractUser, AnonymousUser], msg: Optional[str] = None):
    if not check_superuser(user):
        raise PermissionDenied(msg or "You don't have permissions to do this...")


def check_perms(
    user: Union[AbstractUser, AnonymousUser],
    perms: List[str],
    any_perm: bool = True,
    with_superuser: bool = True,
):
    if not check_authenticated(user):
        return False

    if with_superuser and check_superuser(user):
        return True

    u_perms = set(user.get_all_permissions())
    f = any if any_perm else all
    return f(p in u_perms for p in perms)


def assert_perms(
    user: Union[AbstractUser, AnonymousUser],
    perms: List[str],
    any_perm: bool = True,
    with_superuser: bool = True,
    msg: Optional[str] = None,
):
    if not check_perms(user, perms, any_perm=any_perm, with_superuser=with_superuser):
        raise PermissionDenied(msg or "You don't have permissions to do this...")
