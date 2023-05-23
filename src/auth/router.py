from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from database import get_async_session

from .models import Role, User

from .schemas import RoleReadWithUsers, RoleRead

router = APIRouter(tags=['roles'], prefix='/role')


@router.get('/{role_id}', response_model=RoleReadWithUsers)
async def get_role(role_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Role).where(Role.id == role_id).options(selectinload(Role.users))
    result = await session.execute(query)
    role = result.scalars().first()
    return role


@router.get('/')
async def get_users_roles(role_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.role_id == role_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post('/')
async def create_role(db: AsyncSession = Depends(get_async_session)):
    stmt = insert(Role).values(name='user', permission=None)
    await db.execute(stmt)
    await db.commit()
    return {'success': 'status'}

