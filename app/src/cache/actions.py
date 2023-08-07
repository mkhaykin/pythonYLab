import json
from typing import TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.src.database import Base

from .conn import client

DISH_PRICE_ENCODER = {float: lambda x: f'{round(float(x), 2):.2f}'}
T = TypeVar('T', bound=Base)


async def cache_reset():
    await client.flushall(asynchronous=True)


async def cache_set(key: UUID | str, value: T) -> None:
    data = jsonable_encoder(value.__dict__, custom_encoder=DISH_PRICE_ENCODER)
    await client.set(str(key), json.dumps(data), ex=30)
    return


async def cache_get(key: UUID | str) -> dict | None:
    data = await client.get(str(key))
    if data:
        return json.loads(data)
    return None


async def cache_del(key: UUID | str) -> None:
    await client.delete(str(key))
    return