# -*- coding: utf-8 -*-
"""
Created on 2021/2/8 11:28 上午

@Author: fduxuan

Desc:

"""
import uvicorn
from fastapi import FastAPI, Request
from error import register_error
from router import register_router
from config import register_db

app = FastAPI()
# 注册数据库
register_db(app)

# 注册异常
register_error(app)

# 注册router
register_router(app)


@app.get("/")
async def root(request: Request):
    return 'hello world'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
