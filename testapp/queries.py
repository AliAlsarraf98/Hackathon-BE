import graphene
from django.db.models import QuerySet

from testapp import models
from testapp.types import TestAppType


class TestAppQuery(graphene.ObjectType):
    get_all_test_app = graphene.List(TestAppType)
    get_test_app_by_id = graphene.Field(TestAppType, pk=graphene.Int())

    def resolve_get_test_app_by_id(
        self, info: graphene.ResolveInfo, pk: int
    ) -> models.TestApp:
        return models.TestApp.objects.get(id=pk)

    def resolve_get_all_test_app(
        self, info: graphene.ResolveInfo
    ) -> QuerySet[models.TestApp]:
        return models.TestApp.objects.all()
