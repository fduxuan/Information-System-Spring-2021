# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:47 上午

@Author: fduxuan

Desc:

"""
from .helper import *
from fastapi import APIRouter, Response, Body, File, Form
from error import *
from pydantic import BaseModel, Field
import re
import io
from typing import Optional
from model.base import gen_uuid

department_router = APIRouter(
    prefix="/api/department",
    tags=['department'],
    default_response_class=SuccessResponse
)


@department_router.post('/find')
@valid_token
async def find(request: Request, find_query: FindQuery):
    """ 查询部门 """
    department = mount(request, Department)
    find_query.projection = {"_id": 0}
    lookup = LookUp(from_coll='user', from_field='leader',
                    match_field='email', project={'name': 1, 'avatar': 1, 'email': 1}, output_name='leader_info')
    return await department.find_with_aggregate(find_query, [lookup])


class CreateDepartmentItem(BaseModel):
    name: str = Field(..., description="The name can not be empty", min_length=1)
    leader: str = None


@department_router.post('/create')
@admin_valid_token
async def create(request: Request, department_info: CreateDepartmentItem):
    """ 管理员使用，创建部门 """
    department = mount(request, Department)
    await department.find_one(name=department_info.name)
    if department.id:
        raise EXIST_DEPARTMENT
    if department_info.leader:
        user = mount(request, User)
        await user.find_one(email=department_info.leader)
        if not user.id:
            raise NOT_EXIST_USER
        if user.department:
            orig_department = mount(request, Department)
            await orig_department.from_id(user.department)
            if orig_department.leader == user.email:
                raise INVITE_DEPARTMENT_LEADER
        await department.create(**department_info.dict())
        await user.update_one(department=department.id)
    else:
        await department.create(**department_info.dict())
    return None


@department_router.post('/update')
@admin_valid_token
async def update(request: Request, department: Department):
    """ 更新部门信息 """
    department.connect(request.app.state.mongo_client)
    data = department.data(not_none=True)
    await department.from_id(department.id, error=NOT_EXIST_DEPARTMENT)
    if 'leader' in data and data['leader'] != '':
        user = mount(request, User)
        await user.find_one(email=data['leader'])
        if not user.id:
            raise NOT_EXIST_USER
        if user.department != department.id:
            department2 = mount(request, Department)
            await department2.from_id(user.department, error=NOT_EXIST_DEPARTMENT)
            if department2.leader == user.email:
                await department2.update_one(leader=None, not_none=False)
        await user.update_one(department=department.id)
    if 'name' in data:
        department2 = mount(request, Department)
        await department2.find_one(name=data['name'])
        if department2.id is not None and department2.id != department.id:
            raise EXIST_DEPARTMENT
    await department.update_one(**data)  # you cannot delete a field
    return department.data()


@department_router.get('/show/{department_id}')
@valid_token
async def show(request: Request, department_id: str):
    """ 部门信息 """
    department = mount(request, Department)
    await department.from_id(department_id, error=NOT_EXIST_DEPARTMENT)
    return department.data()


@department_router.get('/{department_id}/invite/{user_email}')
@valid_token
async def invite(request: Request, department_id: str, user_email: str):
    department = mount(request, Department)
    await department.from_id(department_id, error=NOT_EXIST_DEPARTMENT)
    if not request.state.user.admin and request.state.user.email != department.leader:
        raise PERMISSION_DENIED
    user = mount(request, User)
    await user.find_one(email=user_email, to_raise=True, error=NOT_EXIST_USER)
    if user.department:
        orig_department = mount(request, Department)
        await orig_department.from_id(user.department)
        if orig_department.leader == user.email:
            raise INVITE_DEPARTMENT_LEADER
    await user.update_one(department=department_id)
    return user.data()


if __name__ == "__main__":
    pass
