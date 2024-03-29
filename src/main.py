from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse, StreamingResponse
import boto3
# auth
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

# routers
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from auth.router import router as router_auth
from chat.router import app as router_chat

# fastapi_cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from config import REDIS_HOST, REDIS_PORT, YandexS3Config

app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_auth)
app.include_router(router_chat)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YandexS3Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=YandexS3Config.AWS_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)

@app.get('/file')
async def get_file():
    file = s3.get_object(Bucket='rec-and-rem-test', Key='static/globe.png')
    return StreamingResponse(file['Body'])
