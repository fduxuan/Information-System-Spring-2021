# -*- coding: utf-8 -*-
"""
Created on 2021/5/3 8:53 下午

@Author: fduxuan

Desc: 数据库配置

"""
import os
import motor.motor_asyncio
from aioredis import create_redis_pool, Redis
from minio import Minio
from error import *
import io


def get_value_from_env(name, default):
    """
    从环境变量中读取（在dockerfile中引入）
    """
    value = os.environ.get(name, default)
    return value


class DBConfig:
    """
    default 为本地开发环境，生产环境由环境变量引入，避免泄露风险
    """
    mongo_url = get_value_from_env(name='MONGO_URL', default="mongodb://localhost:27017")
    mongo_database = get_value_from_env(name='MONGO_DATABASE', default='testing')
    redis_url = get_value_from_env(name='REDIS_URL', default="redis://localhost:6379")

    def mongo_client(self):
        return motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url, serverSelectionTimeoutMS=1000)

    async def redis_client(self) -> Redis:
        return await create_redis_pool(self.redis_url)


class Mio:
    endpoint = None
    access_key = None
    secret_key = None
    secure = False

    client: Minio = None

    def __init__(self):
        self.endpoint = get_value_from_env('MINIO_ENDPOINT', 'localhost:9000')
        self.access_key = get_value_from_env('MINIO_ACCESS_KEY', 'bobo')
        self.secret_key = get_value_from_env('MINIO_SECRET_KEY', 'bobobobo')
        self.secure = get_value_from_env('MINIO_SECURE', False)
        self.connect()

    def connect(self):
        """
        连接minio
        """
        self.client = Minio(endpoint=self.endpoint,
                            access_key=self.access_key,
                            secret_key=self.secret_key,
                            secure=self.secure)

    def create_bucket(self, bucket_name, location='cn-north-1'):
        """
        创建存储桶，如果存在就不创建
        """
        try:
            if not self.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name=bucket_name, location=location)
        except Exception as e:
            raise UPLOAD_ERROR(reason=f"{e}")

    def remove_bucket(self, bucket_name):
        """ 删除整个桶 谨慎操作 """
        try:
            if self.bucket_exists(bucket_name):
                objects = self.client.list_objects(bucket_name)
                for obj in objects:
                    self.client.remove_object(bucket_name, obj.object_name)
                # self.client.remove_bucket(bucket_name)
        except Exception as e:
            raise UPLOAD_ERROR(reason=f"{e}")

    def bucket_exists(self, bucket_name):
        return self.client.bucket_exists(bucket_name=bucket_name)

    def put_object(self, bucket_name, object_name, data: io.RawIOBase,
                   length, content_type='application/octet-stream', metadata=None):
        """
        上传文件
        """
        try:
            self.client.put_object(bucket_name=bucket_name,
                                   object_name=object_name,
                                   data=data,
                                   length=length,
                                   content_type=content_type,
                                   metadata=metadata)
        except Exception as e:
            raise UPLOAD_ERROR(reason=f"{e}")

    def get_object(self, bucket_name, object_name):
        try:
            data = self.client.get_object(bucket_name, object_name)
            return data
        except Exception as e:
            raise DOWNLOAD_ERROR

    def remove_object(self, bucket_name, object_name):
        try:
            data = self.client.remove_object(bucket_name, object_name)
            return data
        except:
            pass


if __name__ == "__main__":
    pass
