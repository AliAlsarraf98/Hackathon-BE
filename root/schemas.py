import graphene
from graphql_auth.schema import MeQuery

from hackathon.queries import HackathonQuery
from testapp.mutations import TestAppMutation
from testapp.queries import TestAppQuery
from users.mutations import AuthMutation


class Query(TestAppQuery, HackathonQuery, MeQuery, graphene.ObjectType):
    test = graphene.String()

    def resolve_test(self, info: graphene.ResolveInfo) -> str:
        return "Hello World!"


class Mutation(TestAppMutation, AuthMutation, graphene.ObjectType):
    pass


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
