# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:47 上午

@Author: fduxuan

Desc:

"""
from .helper import *
from fastapi import APIRouter, Response, Body, UploadFile, File, Form
from error import *
from pydantic import BaseModel, Field
import re
import io
from typing import Optional
from model.base import gen_uuid

user_router = APIRouter(
    prefix="/api/user",
    tags=['user'],
    default_response_class=SuccessResponse
)


DEFAULT_AVATAR = "https://minio.droproblem.com/avatar2/default.jpg"


@user_router.get('/info')
@valid_token
async def info(request: Request):
    """ 获得用户信息 """
    return request.state.user.data(exclude={'password'})


@user_router.post('/login')
async def login(request: Request, response: Response,
                email: str = Body(..., min_length=1),
                password: str = Body(..., min_length=1)):
    """ 登录 """
    user = mount(request, User)
    await user.find_one(to_raise=True, error=LOGIN_ERROR, email=email, password=password)

    access_token = gen_token()
    await redis_set(request=request, key=str(access_token), value=user.id, expire=60 * 60 * 24 * 7)
    response.set_cookie(key="access_token", value=access_token)

    return user.data(exclude={'password'})


@user_router.post('/logout')
@valid_token
async def logout(request: Request):
    """ 退出登录 """
    await redis_delete(request, request.state.access_token)
    return None


@user_router.post('/find')
@valid_token
async def find(request: Request, find_query: FindQuery):
    """ 查询用户 """
    user = mount(request, User)
    find_query.projection = {'password': 0, "_id": 0}
    # lookup = LookUp(from_coll='user', from_field='leader',
    #                 match_field='_id', project={'name': 1}, output_name='leader_info')
    lookup = LookUp(from_coll='department', from_field='department',
                    match_field='_id', project={'name': 1}, output_name='department_info')
    return await user.find_with_aggregate(find_query, [lookup])


class CreateUserItem(BaseModel):
    email: str = Field(..., description="The email can not be empty", min_length=1)
    name: str = Field(..., description="The name can not be empty", min_length=1)
    gender: str = 'male'
    position: str = None
    leader: str = None
    admin: bool = False
    department: str = None


@user_router.post('/create')
@admin_valid_token
async def create(request: Request, user_info: CreateUserItem):
    """ 管理员使用，创建用户 / 初始化默认密码为邮箱"""
    user = mount(request, User)
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(regex, user_info.email):
        raise EMAIL_FORMAT_ERROR
    await user.find_one(email=user_info.email)
    if user.id:
        raise EXIST_EMAIL
    user.password = user_info.email
    user.avatar = DEFAULT_AVATAR   # default avatar
    await user.create(**user_info.dict())
    return None


@user_router.post('/update')
@admin_valid_token
async def update(request: Request, user: User):
    """ 更新用户信息 """
    user.connect(request.app.state.mongo_client)
    data = user.data(not_none=True)
    await user.from_id(user.id, error=NOT_EXIST_USER)
    # user2 = mount(request, User)
    # await user2.find_one(email=data['email'])
    # if user2.id is not None and user2.id != user.id:
    #     raise EXIST_USER
    if 'email' in data:
        data.pop('email')
    await user.update_one(**data)
    return user.data(exclude={'password'})


@user_router.post('/reset/{user_id}')
@admin_valid_token
async def reset_password(request: Request, user_id: str):
    """
    用户忘记密码时，管理员帮忙重置密码为邮箱号
    """
    user = mount(request, User)
    await user.from_id(user_id, error=NOT_EXIST_USER)
    await user.update_one(password=user.email)
    return None


@user_router.get('/show/{user_id}')
@valid_token
async def show(request: Request, user_id: str):
    """ 用户信息 """
    user = mount(request, User)
    await user.from_id(user_id, error=NOT_EXIST_USER)
    return user.data(exclude={'password'})


@user_router.post('/change/avatar')
@valid_token
async def change_avatar(request: Request, file: UploadFile = File(...), user_id: str = Form(..., min_length=1)):
    """ 修改头像 """
    user = request.state.user
    if user_id != user.id:
        raise NO_PRIVILEGE
    storage = request.app.state.minio
    storage.create_bucket(bucket_name='avatar2')
    suffix = gen_uuid()+".jpg"
    content = await file.read()

    with io.BytesIO(content) as f:
        if user.avatar != DEFAULT_AVATAR and not user.avatar:
            storage.remove_object(bucket_name='avatar2', object_name=f'{user.avatar.split(f"{storage.endpoint}/avatar2/")[-1]}')
        storage.put_object(bucket_name='avatar2', object_name=f'{suffix}', data=f, length=len(content))
    await user.update_one(avatar=f"https://{storage.endpoint}/avatar2/{suffix}")
    return user.data(exclude={'password'})


if __name__ == "__main__":
    pass
