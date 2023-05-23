import orjson

from typing import Optional, List, Union, Any, Dict
from pydantic import BaseModel
from fastapi_users import schemas
from sqlalchemy import JSON


class RoleRead(BaseModel):
    id: int
    name: str
    permissions: Union[List, Dict[Any, Any], None] = None

    class Config:
        orm_mode = True


class RoleReadWithUsers(RoleRead):
    users: List['UserRead']

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


RoleReadWithUsers.update_forward_refs()






