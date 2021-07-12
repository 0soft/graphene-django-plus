"""
Settings for graphene-django-plus are all namespaced in the GRAPHENE_DJANGO_PLUS setting.
For example your project's `settings.py` file might look like this:
GRAPHENE_DJANGO_PLUS = {
    'MUTATIONS_INCLUDE_REVERSE_RELATIONS': False
}
This module provides the `graphene_django_plus_settings` object, that is used to access
graphene-django-plus settings, checking for user settings first, then falling
back to the defaults.
"""
import importlib

from django.conf import settings
from django.test.signals import setting_changed

# Copied shamelessly from Django REST Framework and graphene-django

DEFAULTS = {
    "MUTATIONS_INCLUDE_REVERSE_RELATIONS": True,
    "MUTATIONS_SWALLOW_PERMISSION_DENIED": True,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split(".")
        module_path, class_name = ".".join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}' for graphene-django-plus setting '{}'. {}: {}.".format(
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class GrapheneDjangoPlusSettings:
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:
        from graphene_django_plus.settings import settings
        print(settings.MUTATIONS_INCLUDE_REVERSE_RELATIONS)
    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "GRAPHENE_DJANGO_PLUS", {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid graphene-django-plus setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val


graphene_django_plus_settings = GrapheneDjangoPlusSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_graphene_django_plus_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "GRAPHENE_DJANGO_PLUS":
        graphene_django_plus_settings.reload()


setting_changed.connect(reload_graphene_django_plus_settings)
