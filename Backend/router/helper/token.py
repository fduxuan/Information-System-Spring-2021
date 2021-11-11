# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:54 上午

@Author: fduxuan

Desc:

"""
import datetime
import os
import hashlib
from fastapi import Request
from error import *
from .operator import *


def gen_token():
    """
    使用时间戳和随机数生成唯一token
    """
    bs = str(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).encode()
    bs += os.urandom(16)
    return hashlib.sha1(bs).hexdigest()


async def get_token(request: Request):
    """
    从request header中获取cookie,并转化为键值对,获取accesstoken
    """
    cookie = request.headers.get('cookie')
    if cookie is None:
        raise NOT_LOGIN
    cookies = dict([x.split("=", 1) for x in cookie.split("; ")])
    access_token = cookies.get('access_token', None)

    # 未携带token参数的请求
    if access_token is None:
        raise NOT_LOGIN

    # token 过期或者因为修改密码等操作而导致的无效
    user_id = await redis_get(request, access_token)
    if user_id is None:
        raise NOT_LOGIN

    return access_token, user_id


if __name__ == "__main__":
    pass
