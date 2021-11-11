# -*- coding: utf-8 -*-
"""
Created on 2021/5/24 1:33 下午

@Author: fduxuan

Desc:

"""
from fastapi import APIRouter, Request, Body
from .helper import *
from model import *
from error import *


relation_router = APIRouter(
    prefix="/api/relation",
    tags=['relation'],
    default_response_class=SuccessResponse
)


# @relation_router.post('/create')
# @admin_valid_token
# async def create(request: Request, from_uid: str = Body(..., min_length=1), to_uid: str = Body(..., min_length=1),
#                  ship: str = Body(..., regex="^(leadership|supporting)$")):
#     """ 创建用户关系，管理员使用 """

#     relation = mount(request, Relation)
#     user = mount(request, User)
#     await user.from_id(from_uid, error=NOT_EXIST_USER)
#     await user.from_id(to_uid, error=NOT_EXIST_USER)
#     await relation.find_one(from_uid=from_uid, to_uid=to_uid)
#     if relation.id:
#         raise DUPLICATE_RELATION
#     await relation.create(from_uid=from_uid, to_uid=to_uid, ship=ship)
#     return relation.data()


@relation_router.get('/find/{uid}')
@valid_token
async def find(request: Request, uid: str):
    """ 查询relation，聚合返回姓名等信息 """

    # relation = mount(request, Relation)

    # lookup1 = LookUp(from_coll='user', from_field='from_uid',
    #                  match_field='_id', project={'name': 1, 'avatar': 1}, output_name='from_info')
    # lookup2 = LookUp(from_coll='user', from_field='to_uid',
    #                  match_field='_id', project={'name': 1, 'avatar': 1}, output_name='to_info')

    # return await relation.find_with_aggregate(find_query, [lookup1, lookup2])

    user = mount(request, User)
    await user.from_id(uid, error=NOT_EXIST_USER)
    if user.department is None:
        return {
            "count": 0,
            "results": []
        }
    res = []
    department = mount(request, Department)
    await department.from_id(user.department)
    query = FindQuery()
    query.filter = {'department': department.id}
    query.projection = {'name': 1, 'avatar': 1, 'email': 1}
    colleagues = await user.find(query)
    colleagues = colleagues['results']
    department = department.data()
    for colleage in colleagues:
        res.append({
            "from_info": department,
            "to_info": colleage
        })
    return {
        "count": len(res),
        "results": res
    }


# @relation_router.post('/delete')
# @admin_valid_token
# async def delete(request: Request, find_query: FindQuery):
#     """ 删除 """
#     relation = mount(request, Relation)
#     await relation.delete_many(find_query.filter)


if __name__ == "__main__":
    pass
