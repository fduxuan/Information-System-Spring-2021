# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 12:34 下午

@Author: fduxuan

Desc:

"""
import datetime
import os
import base64
from pydantic import BaseModel
from typing import Any
import motor.motor_asyncio
import motor.core
from config import DBConfig
import copy
from error import *
from copy import deepcopy


def get_now():
    """ utc 时间 """
    return datetime.datetime.utcnow()+datetime.timedelta(hours=8)


def gen_uuid():
    """ 生成唯一ID """
    bs = str(get_now()).encode()
    bs += os.urandom(32)
    return base64.urlsafe_b64encode(bs).decode().replace("=", "")


def rewrite_field(s: str):
    while len(s) > 0 and s.startswith('_'):
        s = s[1:]
    assert len(s) > 0
    return s


class FindQuery(BaseModel):
    """
    find 参数封装
    filter: 查询参数
    projection: 投影
    limit: 数目限制，默认100条
    skip: 略过，默认0
    sort: 排序，默认安装创建时间降序
    """
    filter: dict = None
    projection: dict = None
    limit: int = 100
    skip: int = 0
    sort: Any = [("created_at", -1)]


class LookUp(BaseModel):
    """ 用于连表查询的封装
    ex:
    {"$lookup": {
            "from": 'user',
            "let": {'from_uid': '$from_uid'},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$$from_uid", "$_id"]}}},
                {'$project': {"name": 1}}
            ],
            'as': 'from_info'
        }},
    """
    from_coll: str
    from_field: str
    match_field: str
    project: dict = {}
    output_name: str

    def data(self):
        res = {"$lookup": {
                    "from": self.from_coll,
                    "let": {rewrite_field(self.from_field): f'${self.from_field}'},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": [f"$${rewrite_field(self.from_field)}", f"${self.match_field}"]}}},
                        {'$project': self.project}
                    ],
                    'as': self.output_name
              }}
        return res







class DataModel(BaseModel):
    """
    对所有mongo collection中存储数据进行封装，并将创建删除函数等进行封装
    """
    db_name: str = DBConfig().mongo_database
    coll_name: str = None
    coll: Any = None

    id: str = None
    created_at: str = None
    update_at: str = None
    deleted_at: str = None

    exclude: set = {'db_name', 'coll_name', 'client', 'coll', 'exclude'}

    def connect(self, client: motor.motor_asyncio.AsyncIOMotorClient):
        """ get the collection """
        self.coll: motor.core.AgnosticCollection = client[self.db_name][self.coll_name]

    def set(self, **kwargs):
        fields = self.data().keys()
        for key, value in kwargs.items():
            if key in fields:
                if value != "":
                    self.__setattr__(key, value)

    def data(self, exclude: set = None, not_none=False) -> dict:
        """
        return basic field as dict format
        not_none == true => value is not None
        """
        if not exclude:
            exclude = self.exclude
        else:
            exclude.update(self.exclude)
        data = self.dict(exclude=exclude)
        res = copy.deepcopy(data)
        if not_none:
            for key, value in data.items():
                if value is None:
                    res.pop(key)
        return res

    async def create(self, **kwargs):
        """ 创建 """
        self.set(
            created_at=get_now().isoformat(),
            id=gen_uuid(),
            **kwargs
        )
        data = self.data(not_none=True)
        data["_id"] = self.id
        data.pop('id')
        return await self.coll.insert_one(data)

    async def find_one(self, to_raise=False, error=UNKNOWN_ERROR, **kwargs):
        obj = await self.coll.find_one(
            filter=kwargs
        )
        if not obj:
            if to_raise:
                raise error
        else:
            obj['id'] = obj["_id"]
            self.set(**obj)

    async def from_id(self, data_id, to_raise=True, error=UNKNOWN_ERROR):
        await self.find_one(_id=data_id, to_raise=to_raise, error=error)

    async def find(self, find_query: FindQuery):
        """
        max(limit) = 1000 to ensure speed
        """
        if find_query.filter is None:
            find_query.filter = {}
        find_query.limit = min(find_query.limit, 1000)
        cursor = self.coll.find(
            filter=find_query.filter,
            projection=find_query.projection,
            skip=find_query.skip,
            limit=find_query.limit,
            sort=find_query.sort
        )
        count_ = await self.coll.count_documents(filter=find_query.filter)
        results = await cursor.to_list(find_query.limit)
        for i in range(0, len(results)):
            results[i]['id'] = results[i]['_id']
            results[i].pop('_id')
        return {
            'count': count_,
            'results': results
        }

    async def update_one(self, not_none=True, **kwargs):
        self.set(**kwargs)
        self.set(update_at=get_now().isoformat())
        exclude = kwargs.get('exclude', {'id', 'created_at'})
        data = self.data(exclude=exclude, not_none=not_none)
        return await self.coll.update_one({'_id': self.id}, {"$set": data})

    async def aggregate(self, pipeline: list, count=100):
        res = self.coll.aggregate(pipeline)
        return await res.to_list(count)

    async def count(self, find_query: FindQuery):
        query = {}
        if find_query.filter:
            query = find_query.filter
        return await self.coll.count_documents(filter=query)

    async def find_with_aggregate(self, find_query: FindQuery, lookup: [LookUp]):
        """ 用聚合查询find的东西 """
        pipeline = [
            {"$skip": find_query.skip},
            {"$limit": find_query.limit},
        ]

        if find_query.sort:
            pipeline.insert(0, {"$sort": {k: v for k, v in find_query.sort}})
        
        if find_query.filter:
            pipeline.insert(0, {"$match": find_query.filter})
        for l in lookup:
            pipeline.append(l.data())

        pipeline.append({"$addFields": {'id': '$_id'}})

        if find_query.projection:
            pipeline.append({"$project": find_query.projection})

        count = await self.count(find_query)
        res = self.coll.aggregate(pipeline)
        res = await res.to_list(count)
        return {
            'count': count,
            'results': res
        }

    async def delete_many(self, query):
        await self.coll.delete_many(query)

if __name__ == "__main__":
    pass
