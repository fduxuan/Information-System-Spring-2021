# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:30 上午

@Author: fduxuan

Desc:

"""
from fastapi import Response, Request
import typing
import json
from functools import wraps
from .operator import *
from .token import *
from model import *


class SuccessResponse(Response):
    """
    重构JSONResponse, 在API router中设定为default response class，统一返回格式
    """
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            {'code': 0, 'data': content},
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


def valid_token(func):
    """
    从header的cookie中解析出合法token
    """
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        request: Request = kwargs['request']
        access_token, user_id = await get_token(request)

        user = mount(request, User)
        await user.from_id(user_id, error=NOT_EXIST_USER)
        request.state.user = user
        request.state.access_token = access_token
        request.state.user_id = user_id
        kwargs['request'] = request
        return await func(*args, **kwargs)
    return decorated_function


def admin_valid_token(func):
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        request: Request = kwargs['request']
        access_token, user_id = await get_token(request)

        user = mount(request, User)
        await user.from_id(user_id, error=NOT_EXIST_USER)
        request.state.user = user
        if not user.admin:
            raise NOT_ADMIN
        request.state.access_token = access_token
        request.state.user_id = user_id
        kwargs['request'] = request
        return await func(*args, **kwargs)

    return decorated_function


if __name__ == "__main__":
    pass
