import graphene
from graphql_jwt.exceptions import PermissionDenied

from users.models import CustomUser


def get_user_from_context(
    info: graphene.ResolveInfo,
) -> CustomUser:
    user = info.context.user
    if user.is_anonymous:
        raise PermissionDenied
    return user
