import graphene

from testapp.mutations import TestAppMutation
from testapp.queries import TestAppQuery
from users.mutations import AuthMutation


class Query(TestAppQuery, graphene.ObjectType):
    test = graphene.String()

    def resolve_test(self, info: graphene.ResolveInfo) -> str:
        return "Hello World!"


class Mutation(TestAppMutation, AuthMutation, graphene.ObjectType):
    pass


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
