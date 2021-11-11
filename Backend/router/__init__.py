# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:28 上午

@Author: fduxuan

Desc:

"""
from .user import user_router
from .relation import relation_router
from .department import department_router
from .task import task_router
from fastapi import FastAPI


def register_router(app: FastAPI):
    app.include_router(user_router)
    app.include_router(relation_router)
    app.include_router(department_router)
    app.include_router(task_router)






if __name__ == "__main__":
    pass
