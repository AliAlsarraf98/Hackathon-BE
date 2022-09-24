import graphene
from django.db.models import QuerySet

from hackathon import models
from hackathon.types import HackathonType
from shared import utils


class HackathonQuery(graphene.ObjectType):
    test_me = graphene.List(HackathonType)

    def resolve_test_me(
        self, info: graphene.ResolveInfo
    ) -> QuerySet[models.Hackathon]:
        utils.get_user_from_context(info)
        return models.Hackathon.objects.all()
