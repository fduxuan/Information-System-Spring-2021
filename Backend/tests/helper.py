# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 1:32 下午

@Author: fduxuan

Desc:

"""
import pymongo
from redis import Redis, ConnectionPool, StrictRedis
from config import DBConfig
from fastapi.testclient import TestClient
from server import app
from error import *


class Result:
    """
    返回结果的封装，方便assert
    """
    code = None
    data = None
    headers = None

    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.data = kwargs.get('data')

    def set(self, **kwargs):
        self.code = kwargs.get('code')
        self.data = kwargs.get('data')

    def __str__(self):
        return f"{self.code}: {self.data}"


class TestDb:
    mongo_client = None
    redis: Redis = None
    user: pymongo.collection = None
    relation: pymongo.collection = None
    daily: pymongo.collection = None

    def __init__(self):
        # mongo 连接
        db_config = DBConfig()
        mongo_url = db_config.mongo_url
        self.mongo_client = pymongo.MongoClient(mongo_url)
        database = self.mongo_client.get_database(db_config.mongo_database)

        self.user = database['user']
        self.relation = database['relation']
        self.daily = database['daily']

        # redis 连接
        redis_url = db_config.redis_url
        pool = ConnectionPool.from_url(redis_url)
        self.redis = StrictRedis(connection_pool=pool)

    def fake_user(self, **kwargs):
        self.user.insert_one(kwargs)

    def fake_relation(self, **kwargs):
        self.relation.insert_one(kwargs)

    def fake_daily(self, **kwargs):
        self.daily.insert_one(kwargs)

    def redis_set(self, key, value, ex=60*10):
        self.redis.set(key, value, ex)

    def redis_delete(self, key):
        if self.redis.exists(key):
            self.redis.delete(key)

    def redis_clear(self):
        for elem in self.redis.keys():
            self.redis.delete(elem)

    def redis_exist(self, key):
        return self.redis.exists(key)

    def redis_get(self, key):
        if self.redis.exists(key):
            return self.redis.get(key)
        return None

    def fake_admin_login_user(self):
        self.user.delete_one({"_id": "login_admin_user"})
        self.redis_delete('fake_access_token')
        self.user.insert_one({"_id": 'login_admin_user', "email": 'admin@qq.com', "name": "admin", 'admin': True})
        self.redis_set('fake_access_token', 'login_admin_user')
        headers['cookie'] = "access_token=fake_access_token"

    def fake_ordinary_login_user(self):
        self.user.delete_one({"_id": "login_ordinary_user"})
        self.redis_delete('fake_ordinary_access_token')
        self.user.insert_one({"_id": 'login_ordinary_user', "email": 'ordinary@qq.com', "name": "ordinary", 'admin': False})
        self.redis_set('fake_ordinary_access_token', 'login_ordinary_user')
        headers['cookie'] = "access_token=fake_ordinary_access_token"


headers = {}


class MyClient:
    prefix = ''
    result = Result()

    def __init__(self, prefix):
        self.prefix = prefix

    def form_result(self, res):
        # 将返回code放在这里校验，减少外部代码
        self.result.set(**res.json())
        self.result.headers = res.headers
        print(f"Your Result: {self.result}")
        return self.result

    def get(self, url, data: dict = None):
        with TestClient(app) as client:
            print(f"\n--------------------\n{self.prefix}{url}")
            res = client.get(url=f"{self.prefix}{url}", data=data, headers=headers)
            return self.form_result(res)

    def post(self, url, data: dict = None, files: dict = None, form: dict = None):
        if data is None:
            data = {}
        with TestClient(app) as client:
            print(f"\n--------------------\n{self.prefix}{url}")
            res = client.post(url=f"{self.prefix}{url}", json=data, headers=headers, files=files, data=form)
            return self.form_result(res)


if __name__ == "__main__":
    pass
