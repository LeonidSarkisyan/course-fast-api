from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Operation
from .decorators import permission, is_exist

from auth.models import User


class OperationDB:

    @staticmethod
    @is_exist
    @permission(roles=['user', 'moderator', 'admin'])
    async def get_operation_by_id(operation_id: int, user: User, session: AsyncSession):
        query = select(Operation).where(Operation.id == operation_id)
        result = await session.execute(query)
        return result.mappings().all()

    @staticmethod
    @is_exist
    @permission(roles=['user', 'moderator', 'admin'])
    async def get_list_operation(operation_type: str | None, session: AsyncSession):
        if operation_type:
            query = select(Operation).where(Operation.type == operation_type)
        else:
            query = select(Operation)
        result = await session.execute(query)
        return result.mappings().all()

    @staticmethod
    @permission
    async def delete_operation_by_id(operation_id: int, user: User, session: AsyncSession):
        stmt = delete(Operation).where(Operation.id == operation_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
