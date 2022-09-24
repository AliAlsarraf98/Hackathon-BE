import graphene_django

from hackathon import models


class HackathonType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.Hackathon
