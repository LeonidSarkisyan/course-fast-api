from .exception import NoExistOperation, NoRights

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, Role

def is_exist(func):
    """ Если записей нет, то возвращается исключение NoExistOperation"""
    async def wrapper(*args):
        result = await func(*args)
        if result:
            return result
        else:
            raise NoExistOperation

    return wrapper


def permission(roles: list):
    def decorator(func):
        async def wrapper(*args):
            for i in args:
                if type(i) == User:
                    user: User = i
                    if user.role_id != 2:
                        raise NoRights
            result = await func(*args)
            return result
        return wrapper
    return decorator

