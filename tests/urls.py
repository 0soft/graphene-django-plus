from django.urls import path

from graphene_django_plus.views import GraphQLView

from .schema import schema

urlpatterns = [
    path(r"graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
]
