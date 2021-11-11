# -*- coding: utf-8 -*-
"""
Created on 2021/5/3 8:53 下午

@Author: fduxuan

Desc:

"""
from fastapi import FastAPI
from .database import DBConfig, Mio


def register_db(app: FastAPI):
    """
    注册数据库
    """
    @app.on_event("startup")
    async def startup_event():
        """
        连接数据库
        """
        db_config = DBConfig()
        app.state.mongo_client = db_config.mongo_client()
        app.state.redis = await db_config.redis_client()
        mio = Mio()
        app.state.minio = mio

    @app.on_event("shutdown")
    async def shutdown_event():
        """
        关闭数据库连接，防止内存泄漏
        """
        app.state.mongo_client.close()
        app.state.redis.close()


if __name__ == "__main__":
    pass
