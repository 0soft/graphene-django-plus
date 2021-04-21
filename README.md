# graphene-django-plus #

[![build status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2F0soft%2Fgraphene-django-plus%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/0soft/graphene-django-plus/goto?ref=master)
[![docs status](https://img.shields.io/readthedocs/graphene-django-plus.svg)](https://graphene-django-plus.readthedocs.io)
[![coverage](https://img.shields.io/codecov/c/github/0soft/graphene-django-plus.svg)](https://codecov.io/gh/0soft/graphene-django-plus)
[![PyPI version](https://img.shields.io/pypi/v/graphene-django-plus.svg)](https://pypi.org/project/graphene-django-plus/)
![python version](https://img.shields.io/pypi/pyversions/graphene-django-plus.svg)
![django version](https://img.shields.io/pypi/djversions/graphene-django-plus.svg)

Tools to easily create permissioned CRUD endpoints in [graphene-django](https://github.com/graphql-python/graphene-django).

## Install

```bash
pip install graphene-django-plus
```

To make use of everything this lib has to offer, it is recommended to install
both [graphene-django-optimizer](https://github.com/tfoxy/graphene-django-optimizer)
and [django-guardian](https://github.com/django-guardian/django-guardian).

```bash
pip install graphene-django-optimizer django-guardian
```

## What it does

* Provides some base types for Django Models to improve querying them with:
    * Unauthenticated user handling
    * Automatic optimization using [graphene-django-optimizer](https://github.com/tfoxy/graphene-django-optimizer)
    * Permission handling for queries using the default [django permission system](https://docs.djangoproject.com/en/2.2/topics/auth/default/#topic-authorization)
    * Object permission handling for queries using [django guardian](https://github.com/django-guardian/django-guardian)
    * Relay id conversion so querying can use the global id instead of the model's id
* Provides a set of complete and simple CRUD mutations with:
    * Unauthenticated user handling
    * Permission handling using the default [django permission system](https://docs.djangoproject.com/en/2.2/topics/auth/default/#topic-authorization)
    * Object permission handling using [django guardian](https://github.com/django-guardian/django-guardian)
    * Automatic input generation based on the model (no need to write your own input type or use `django forms` and `drf serializers`)
    * Automatic model validation based on the model's validators
* Very simple to create some quick CRUD endpoints for your models
* Easy to extend and override functionalities
* File upload handling

## What is included

Check the [docs](https://graphene-django-plus.readthedocs.io) for a complete
api documentation.

### Models

* `graphene_django_plus.models.GuardedModel`: A django model that can be used
  either directly or as a mixin. It will provide a `.has_perm` method and a
  `.objects.for_user` that will be used by `ModelType` described bellow to
  check for object permissions.  some utilities to check.

### Types and Queries

* `graphene_django_plus.types.ModelType`: This enchances
  `graphene_django_plus.DjangoModelType` by doing some automatic `prefetch`
  optimization on setup and also checking for objects permissions on queries
  when it inherits from `GuardedModel`.

* `graphene_django_plus.fields.CountableConnection`: This enchances
  `graphene.relay.Connection` to provide a `total_count` attribute.

Here is an example describing how to use those:

```py
import graphene
from graphene import relay
from graphene_django.fields import DjangoConnectionField

from graphene_django_plus.models import GuardedModel
from graphene_django_plus.types import ModelType
from graphene_django_plus.fields import CountableConnection


class MyModel(GuardedModel):
    class Meta:
        # guardian permissions for this model
        permissions = [
            ('can_read', "Can read the this object's info."),
        ]

    name = models.CharField(max_length=255)


class MyModelType(ModelType):
    class Meta:
        model = MyModel
        interfaces = [relay.Node]

        # Use our CountableConnection
        connection_class = CountableConnection

        # When adding this to a query, only objects with a `can_read`
        # permission to the request's user will be allowed to return to him
        # Note that `can_read` was defined in the model.
        # If the model doesn't inherid from `GuardedModel`, `guardian` is not
        # installed or this list is empty, any object will be allowed.
        # This is empty by default
        object_permissions = [
            'can_read',
        ]

        # If unauthenticated users should be allowed to retrieve any object
        # of this type. This is not dependant on `GuardedModel` and neither
        # `guardian` and is defined as `False` by default
        allow_unauthenticated = False

        # A list of Django model permissions to check. Different from
        # object_permissions, this uses the basic Django's permission system
        # and thus is not dependant on `GuardedModel` and neither `guardian`.
        # This is an empty list by default.
        permissions = []


class Query(graphene.ObjectType):
    my_models = DjangoConnectionField(MyModelType)
    my_model = relay.Node.Field(MyModelType)
```

This can be queried like:

```graphql
# All objects that the user has permission to see
query {
  myModels {
    totalCount
    edges {
      node {
        id
        name
      }
    }
  }
}

# Single object if the user has permission to see it
query {
  myModel(id: "<relay global ID>") {
    id
    name
  }
}
```

### Mutations

* `graphene_django_plus.mutations.BaseMutation`: Base mutation using `relay`
  and some basic permission checking. Just override its `.perform_mutation` to
  perform the mutation.

* `graphene_django_plus.mutations.ModelMutation`: Model mutation capable of
  both creating and updating a model based on the existence of an `id`
  attribute in the input. All the model's fields will be automatically read
  from Django, inserted in the input type and validated.

* `graphene_django_plus.mutations.ModelCreateMutation`: A `ModelMutation`
  enforcing a "create only" rule by excluding the `id` field from the input.

* `graphene_django_plus.mutations.ModelUpdateMutation`: A `ModelMutation`
  enforcing a "update only" rule by making the `id` field required in the
  input.

* `graphene_django_plus.mutations.ModelDeleteMutation`: A mutation that will
  receive only the model's id and will delete it (if given permission, of
  course).

Here is an example describing how to use those:

```py
import graphene
from graphene import relay

from graphene_django_plus.models import GuardedModel
from graphene_django_plus.types import ModelType
from graphene_django_plus.mutations import (
    ModelCreateMutation,
    ModelUpdateMutation,
    ModelDeleteMutation,
)


class MyModel(GuardedModel):
    class Meta:
        # guardian permissions for this model
        permissions = [
            ('can_write', "Can update this object's info."),
        ]

    name = models.CharField(max_length=255)


class MyModelType(ModelType):
    class Meta:
        model = MyModel
        interfaces = [relay.Node]


class MyModelUpdateMutation(ModelUpdateMutation):
    class Meta:
        model = MyModel

        # Make sure only users with the given permissions can modify the
        # object.
        # If the model doesn't inherid from `GuardedModel`, `guardian` is not
        # installed ot this list is empty, any object will be allowed.
        # This is empty by default.
        object_permissions = [
            'can_write',
        ]

        # If unauthenticated users should be allowed to retrieve any object
        # of this type. This is not dependant on `GuardedModel` and neither
        # `guardian` and is defined as `False` by default
        allow_unauthenticated = False

        # A list of Django model permissions to check. Different from
        # object_permissions, this uses the basic Django's permission system
        # and thus is not dependant on `GuardedModel` and neither `guardian`.
        # This is an empty list by default.
        permissions = []


class MyModelDeleteMutation(ModelDeleteMutation):
    class Meta:
        model = MyModel
        object_permissions = [
            'can_write',
        ]


class MyModelCreateMutation(ModelCreateMutation):
    class Meta:
        model = MyModel

    @classmethod
    def after_save(cls, info, instance, cleaned_input=None):
        # If the user created the object, allow him to modify it
        assign_perm('can_write', info.context.user, instance)


class Mutation(graphene.ObjectType):
    my_model_create = MyModelCreateMutation.Field()
    my_model_update = MyModelUpdateMutation.Field()
    my_model_delete = MyModelDeleteMutation.Field()
```

This can be used to create/update/delete like:

```graphql
# Create mutation
mutation {
  myModelCreate(input: {name: "foobar"}) {
    myModel {
      name
    }
    errors {
      field
      message
    }
  }
}

# Update mutation
mutation {
  myModelUpdate(input: {id: "<relay global ID>" name: "foobar"}) {
    myModel {
      name
    }
    errors {
      field
      message
    }
  }
}

# Delete mutation
mutation {
  myModelDelete(input: {id: "<relay global ID>"}) {
    myModel {
      name
    }
    errors {
      field
      message
    }
  }
}
```

Any validation errors will be presented in the `errors` return value.

To turn off auto related relations addition to the mutation input - set global
`MUTATIONS_INCLUDE_REVERSE_RELATIONS` parameter to `False` in your
`settings.py`:

```
GRAPHENE_DJANGO_PLUS = {
    'MUTATIONS_INCLUDE_REVERSE_RELATIONS': False
}
```

Note: in case reverse relation does not have `related_name` attribute set -
mutation input will be generated as Django itself is generating by appending
`_set` to the lower cased model name - `modelname_set`

## License

This project is licensed under MIT licence (see `LICENSE` for more info)

## Contributing

Make sure to have [poetry](https://python-poetry.org/) installed.

Install dependencies with:

```bash
poetry install
```

Run the testsuite with:

```bash
poetry run pytest
```

Feel free to fork the project and send me pull requests with new features,
corrections and translations. We'll gladly merge them and release new versions
ASAP.
