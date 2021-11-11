# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 12:54 下午

@Author: fduxuan

Desc:

"""
from .base import *


class User(DataModel):
    coll_name = 'user'

    name: str = None
    email: str = None
    password: str = None
    avatar: str = None
    leader: str = None
    admin: bool = None
    position: str = None
    gender: str = None
    region: str = None
    department: str = None


class Relation(DataModel):
    coll_name = 'relation'

    from_uid: str = None
    to_uid: str = None
    ship: str = None


class Department(DataModel):
    coll_name = 'department'

    name: str = None
    leader: str = None


class Task(DataModel):
    coll_name = 'task'

    name: str = None
    description: str = None
    leader: str = None  # user email
    priority: str = None
    start_date: str = None
    end_date: str = None
    status: str = None
    
    sibling: str = None  # task id. next sibling
    child: str = None  # task id. next child
    parent: str = None  # task id. if root => None
    root: str = None  # task id. if root => root itself


class Participation(DataModel):
    coll_name = 'participation'
    
    user: str = None  # user email
    task: str = None  # task id
    flag: bool = True  # False if deleted


class Comment(DataModel):
    coll_name = 'comment'

    user: str = None  # user email
    task: str = None  # task id
    text: str = None
    attachment: str = None  # path
    datetime: str = None


class Review(DataModel):
    coll_name = 'review'

    type: int = 0  # 0: approve task, 1: task leader appointment, 2: task participant invitaion
    task: str = None  # task id
    submitted_user: str = None  # user email
    submitted_datetime: str = None
    target_user: str = None  # user email
    reply_datetime: str = None
    status: int = 0  # 1: approved; -1: denied


if __name__ == "__main__":
    pass
