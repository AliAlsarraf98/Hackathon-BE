from typing import Any

import graphene
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from testapp import models
from testapp.types import TestAppType


class CreateTestApp(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        image = Upload(required=True)

    test_app = graphene.Field(TestAppType)

    def mutate(
        self, info: graphene.ResolveInfo, **kwargs: Any
    ) -> "CreateTestApp":
        test_app = models.TestApp.objects.create(**kwargs)
        return CreateTestApp(test_app=test_app)


class UpdateTestApp(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)
        name = graphene.String()
        image = Upload()

    test_app = graphene.Field(TestAppType)

    def mutate(
        self, info: graphene.ResolveInfo, pk: int, **kwargs: Any
    ) -> "UpdateTestApp":
        try:
            test_app = models.TestApp.objects.get(id=pk)
        except models.TestApp.DoesNotExist as exc:
            raise GraphQLError(str(exc))

        for key, value in kwargs.items():
            setattr(test_app, key, value)
        test_app.save()

        return UpdateTestApp(test_app=test_app)


class DeleteTestApp(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    status = graphene.Boolean()

    def mutate(self, info: graphene.ResolveInfo, pk: int) -> "DeleteTestApp":
        try:
            test_app = models.TestApp.objects.get(id=pk)
        except models.TestApp.DoesNotExist as exc:
            raise GraphQLError(str(exc))

        test_app.delete()

        return DeleteTestApp(status=True)


class TestAppMutation(graphene.ObjectType):
    create_test_app = CreateTestApp.Field()
    update_test_app = UpdateTestApp.Field()
    delete_test_app = DeleteTestApp.Field()
