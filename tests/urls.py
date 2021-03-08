from django.conf.urls import re_path
from graphene_django_plus.views import GraphQLView

from .schema import schema


urlpatterns = [
    re_path(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
]
