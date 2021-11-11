# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 12:19 下午

@Author: fduxuan

Desc:

"""
from fastapi import Request
from aioredis import Redis


async def redis_get(request: Request, key):
    redis: Redis = request.app.state.redis
    data = await redis.get(key)
    if data:
        return data.decode()
    else:
        return None


async def redis_set(request: Request, key, value, expire):
    redis: Redis = request.app.state.redis
    await redis.set(key=key, value=value, expire=expire)


async def redis_delete(request: Request, key):
    redis: Redis = request.app.state.redis
    await redis.delete(key)


def mount(request: Request, cast):
    mongo_client = request.app.state.mongo_client
    model = cast()
    model.connect(mongo_client)
    return model


if __name__ == "__main__":
    pass
