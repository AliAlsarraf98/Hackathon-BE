import graphene
import graphene_django

from testapp import models


class TestAppType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.TestApp

    image_url = graphene.String()

    def resolve_image_url(self, info: graphene.ResolveInfo) -> str:
        return info.context.build_absolute_uri(self.image.url)
