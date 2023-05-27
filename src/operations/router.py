import time
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from database import get_async_session

from operations.models import Operation
from operations.schemas import OperationCreate, OperationRead, OperationUpdate
from operations.service import OperationDB
from operations.exception import NoExistOperation

from auth.base_config import current_user
from auth.models import User

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.post('/file')
def create_file():
    open("txt.txt", 'w')
    return "File created"

@router.get('/{operation_id}')
async def get_operation(
        operation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    result = await OperationDB.get_operation_by_id(operation_id, user, session)
    return result


@router.get("/")
async def get_specific_operations(
        operation_type: str | None = None,
        session: AsyncSession = Depends(get_async_session),
):
    result = await OperationDB.get_list_operation(operation_type, session)
    return result


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.patch('/{operation_id}')
async def update_operations(
        operation_id: int,
        operation_update: OperationUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    # data = {key: value for key, value in operation_update.dict().items() if value}
    stmt = update(Operation).where(Operation.id == operation_id).values(**operation_update.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete('/{operation_id}')
async def update_operations(
        operation_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    result = await OperationDB.delete_operation_by_id(operation_id, user, session)
    return result

