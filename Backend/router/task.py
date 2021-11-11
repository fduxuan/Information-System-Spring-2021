# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:47 上午

@Author: fduxuan

Desc:

"""
from os import read, stat
from urllib.parse import quote

from starlette.responses import StreamingResponse
from .helper import *
from fastapi import APIRouter, Response, Body, UploadFile, File, Form
from error import *
from pydantic import BaseModel, Field
import re
import io
from typing import Optional
from model.base import gen_uuid
from datetime import datetime
import time


ENABLE_PERMISSION_CHECK = True


task_router = APIRouter(
    prefix="/api/task",
    tags=['task'],
    default_response_class=SuccessResponse
)


DEFAULT_AVATAR = "https://minio.droproblem.com/avatar2/default.jpg"


def convert_node_to_dict(node, children_field=False):
    res = {
        'id': node['id'],
        'key': node['id'],
        'name': node['name'],
        'title': node['name'],
        'scopedSlots': {'title': 'custom'},
        'description': node['description'],
        'leader': node['leader'],
        'priority': node['priority'],
        'start_date': node['start_date'],
        'end_date': node['end_date'],
        'status': node['status'],
        # 'root': node['root'],
        'parent': node.get('parent', None)
    }
    if 'leader_info' in node:
        res['leader_info'] = node['leader_info'][0]
    if 'child_info' in node:
        res['child_info'] = node['child_info']
    if 'participants' in node:
        res['participants'] = node['participants']
    if children_field:
        res['children'] = []
    return res


def assemble_tree_dfs(node_id, node_dict):
    node = node_dict[node_id]
    res = convert_node_to_dict(node, children_field=True)
    child_ptr = node.get('child', None)
    while child_ptr is not None:
        res['children'].append(assemble_tree_dfs(child_ptr, node_dict))
        child_ptr = node_dict[child_ptr].get('sibling', None)
    return res


@task_router.get('/project/info/{project_id}')
@valid_token
async def project_info(request: Request, project_id: str):
    """ 获得项目（树）信息 """
    task = mount(request, Task)
    await task.from_id(project_id, error=NOT_EXIST_PROJECT)
    if task.root != project_id or task.parent is not None:
        raise NOT_EXIST_PROJECT
    query = FindQuery()
    query.filter = {'root': project_id}
    nodes = await task.find(query)
    nodes = nodes['results']
    node_dict = {node['id']: node for node in nodes}
    return assemble_tree_dfs(project_id, node_dict)


def flatten_tree_dfs(node, res, statistics, users):
    res.append(node)
    users[node['leader_info']['email']] = node['leader_info']
    for user in node['participants']:
        users[user['user_info'][0]['email']] = user['user_info'][0]
    statistics['total'] += 1
    if node['status'] == '已完成':
        statistics['finished'] += 1
    finished = 0
    total = 0
    for child in node['children']:
        total += 1
        if child['status'] == '已完成':
            finished += 1
        flatten_tree_dfs(child, res, statistics, users)
    node['finished'] = finished
    node['total'] = total

    node['collapsed'] = True
    node['type'] = "task"
    node['parentId'] = node['parent']
    node.pop('parent')

    node['start'] = int(time.mktime(datetime.strptime(node['start_date'], '%Y-%m-%d').timetuple())) * 1000
    if node['status'] == '已完成':
        node['end'] = int(time.mktime(datetime.strptime(node['end_date'], '%Y-%m-%d').timetuple())) * 1000
    else:
        node['end'] = int(time.mktime(datetime.now().timetuple())) * 1000
    node['duration'] = int(time.mktime(datetime.now().timetuple())) * 1000 - node['start']

    node.pop('children')
    node.pop('participants')


@task_router.get('/project/statistics/{project_id}')
@valid_token
async def project_statistics(request: Request, project_id: str):
    """ 获得项目（树）统计 """
    task = mount(request, Task)
    await task.from_id(project_id, error=NOT_EXIST_PROJECT)
    if task.root != project_id or task.parent is not None:
        raise NOT_EXIST_PROJECT
    nodes = task.coll.aggregate([
        {"$match": {"root": project_id}},
        {"$lookup": {
            "from": "user",
            "let": {"leader": "$leader"},
            "pipeline": [
                {"$match": {
                    "$expr": {"$eq": ["$email", "$$leader"]}
                }},
                {"$project": {
                    "_id": 0, "created_at": 0, "update_at": 0,
                    "password": 0, "admin": 0, "position": 0,
                    "gender": 0, "region": 0, "leader": 0
                }},
                {"$lookup": {
                    "from": "department",
                    "let": {"department": "$department"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {"$eq": ["$_id", "$$department"]}
                        }},
                        {"$project": {"created_at": 0, "update_at": 0}}
                    ],
                    "as": "department_info"
                }}
            ],
            "as": "leader_info"
        }},
        {"$lookup": {
            "from": "participation",
            "let": {"task_id": "$_id"},
            "pipeline": [
                {"$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$task", "$$task_id"]},
                            {"$eq": ["$flag", True]}
                        ]
                    }
                }},
                {"$project": {
                    "_id": 0, "created_at": 0, "update_at": 0,
                    "task": 0, "flag": 0
                }},
                {"$lookup": {
                    "from": "user",
                    "let": {"user": "$user"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {"$eq": ["$email", "$$user"]}
                        }},
                        {"$project": {
                            "_id": 0, "created_at": 0, "update_at": 0,
                            "password": 0, "admin": 0, "position": 0,
                            "gender": 0, "region": 0, "leader": 0
                        }},
                        {"$lookup": {
                            "from": "department",
                            "let": {"department": "$department"},
                            "pipeline": [
                                {"$match": {
                                    "$expr": {"$eq": ["$_id", "$$department"]}
                                }},
                                {"$project": {"created_at": 0, "update_at": 0}}
                            ],
                            "as": "department_info"
                        }}
                    ],
                    "as": "user_info"
                }}
            ],
            "as": "participants"
        }
    }])
    node_dict = {node['_id']: {"id": node['_id'], **node} async for node in nodes}
    project_tree = assemble_tree_dfs(project_id, node_dict)
    statistics = {'finished': 0, 'total': 0}
    res = []
    users = {}
    flatten_tree_dfs(project_tree, res, statistics, users)
    departments = {}
    unknown_departments = 0
    for _, user in users.items():
        if len(user['department_info']) > 0:
            departments[user['department_info'][0]['name']] \
                = departments.get(user['department_info'][0]['name'], 0) + 1
        else:
            unknown_departments += 1
    end_date = datetime.strptime(project_tree['end_date'], '%Y-%m-%d')
    cur_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    return {
        "tasks": res,
        # 'users': users, 
        'department_map': departments,
        'unknow_departments': unknown_departments,
        'deadline': (end_date - cur_date).days,
        **statistics,
    }


@task_router.get('/info/{task_id}')
@valid_token
async def task_info(request: Request, task_id: str):
    """ 获得任务信息 """
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)
    if task.root is None:  # deleted task
        raise NOT_EXIST_TASK
    leader = mount(request, User)
    await leader.find_one(email=task.leader, to_raise=True, error=NOT_EXIST_USER)
    query = FindQuery()
    query.filter = {'parent': task_id}
    lookup1 = LookUp(from_coll='user', from_field='leader',
                     match_field='email', project={'name': 1, 'email': 1, 'avatar': 1}, output_name='leader_info')
    lookup2 = LookUp(from_coll='task', from_field='_id',
                     match_field='parent', project={'name': 1, 'status': 1}, output_name='child_info')
    nodes = await task.find_with_aggregate(query, [lookup1, lookup2])
    nodes = nodes['results']
    node_dict = {node['id']: node for node in nodes}
    res = convert_node_to_dict(task.data(), children_field=True)
    res['leader_info'] = {
        'name': leader.name,
        'email': leader.email,
        'avatar': leader.avatar
    }
    child_ptr = task.child
    while child_ptr is not None:
        child = convert_node_to_dict(node_dict[child_ptr])
        child['finished'] = 0
        for sub_task in child['child_info']:
            if sub_task['status'] == '已完成':
                child['finished'] += 1
        child['total'] = len(child['child_info'])
        child.pop('child_info')
        res['children'].append(child)
        child_ptr = node_dict[child_ptr].get('sibling', None)
    query = FindQuery()
    query.filter = {'task': task_id, 'flag': True}
    participation = mount(request, Participation)
    lookup = LookUp(from_coll='user', from_field='user',
                    match_field='email', project={'name': 1, 'email': 1, 'avatar': 1}, output_name='user_info')
    participations = await participation.find_with_aggregate(query, [lookup])
    participations = participations['results']
    res['participants'] = [participant['user_info'][0] for participant in participations]
    return res


@task_router.post('/project/find')
@valid_token
async def project_find(request: Request, find_query: FindQuery):
    """ 查询 """
    participation = mount(request, Participation)
    # find_query.filter['root'] = {'$ne': None}  # not deleted tasks
    # find_query.filter['parent'] = None  # roots or deleted tasks
    # find_query.projection = {"_id": 0, "sibling": 0, "child": 0, "parent": 0, "root": 0}
    # lookup = LookUp(from_coll='user', from_field='leader',
    #                 match_field='email', project={'name': 1, 'email': 1, 'avatar': 1, '_id': 0}, output_name='leader_info')
    # return await task.find_with_aggregate(find_query, [lookup])
    cur_user = request.state.user.email
    # print(cur_user)
    pipeline = [
        {
            "$match": {
                "user": cur_user,
                "flag": True
            }
        },
        {
            "$lookup": {
                "from": "task",
                "let": {"task_id": "$task"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$_id", "$$task_id"]},
                                ]
                            }
                        }
                    },
                    {
                        "$lookup": {
                            "from": "task",
                            "let": {"root_task": "$root"},
                            "pipeline": [
                                {
                                    "$match": find_query.filter
                                },
                                {
                                    "$match": {
                                        "$expr": {
                                            "$and": [
                                                {"$eq": ["$_id", "$$root_task"]},
                                                # {"$eq": ["$parent", None]},
                                                # {"$ne": ["$root", None]}
                                            ]
                                        }
                                    }
                                }
                            ],
                            "as": "root_info"
                        }
                    },
                    {"$unwind": "$root_info"}
                ],
                "as": "task_info"
            }
        },
        {"$unwind": "$task_info"},
        {
            "$group": {
                "_id": "$task_info.root_info._id",
                "project": {"$first": "$task_info.root_info"},
                "cnt": {"$sum": 1}
            }
        },
        {
            "$unionWith": {
                "coll": "task",
                "pipeline": [
                    {
                        "$match": {
                            "leader": cur_user
                        }
                    },
                    {
                        "$lookup": {
                            "from": "task",
                            "let": {"root_task": "$root"},
                            "pipeline": [
                                {
                                    "$match": find_query.filter
                                },
                                {
                                    "$match": {
                                        "$expr": {
                                            "$and": [
                                                {"$eq": ["$_id", "$$root_task"]},
                                                # {"$eq": ["$parent", None]},
                                                # {"$ne": ["$root", None]}
                                            ]
                                        }
                                    }
                                }
                            ],
                            "as": "root_info"
                        }
                    },
                    {"$unwind": "$root_info"},
                    {
                        "$group": {
                            "_id": "$root_info._id",
                            "project": {"$first": "$root_info"},
                            "cnt": {"$sum": 1}
                        }
                    }
                ]
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "project": {"$first": "$project"},
                "cnt": {"$sum": "$cnt"}
            }
        },
        {
            "$project": {
                "project.created_at": 0, "project.update_at": 0,
                "project.sibling": 0, "project.child": 0,
                "project.parent": 0, "project.root": 0
            }
        },
        {
            "$lookup": {
                "from": "user",
                "let": {"leader": "$project.leader"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$email", "$$leader"]
                            }
                        }
                    },
                    {
                        "$project": {
                            "created_at": 0, "update_at": 0, "password": 0,
                            "admin": 0, "position": 0, "gender": 0, "leader": 0,
                            "department": 0, "region": 0
                        }
                    }
                ],
                "as": "project.leader_info"
            }
        },
    ]
    projects = participation.coll.aggregate([
        *pipeline,
        {
            "$group": {
                "_id": None,
                "cnt": {"$sum": 1}
            }
        }
    ])
    cnt = [ans["cnt"] async for ans in projects]
    cnt = cnt[0] if len(cnt) == 1 else 0
    projects = participation.coll.aggregate([
        *pipeline,
        # {"$sort": {"project.created_at": -1}},
        {"$sort": {"project.name": 1}},
        {"$skip": find_query.skip},
        {"$limit": find_query.limit}
    ])
    projects = [project['project'] async for project in projects]
    return {
        "count": cnt,
        "results": projects
    }


@task_router.get('/statistic/{project_id}')
@valid_token
async def statistic(request: Request, project_id: str):
    """ 统计所需所有"""
    task = mount(request, Task)
    await task.from_id(project_id, error=NOT_EXIST_PROJECT)
    find_query = FindQuery(filter={'root': project_id})
    children = await task.find(find_query)
    count = children['count']
    tasks = []
    # gantt 所需字段
    for c in children['results']:

        c['parentId'] = c.get('parent', None)
        c['duration'] = 15 * 24 * 60 * 60 * 1000
        c['start'] = 1624464000000
        c['collapsed'] = True
        c['type'] = "task"
        c['percent'] = 50

        tasks.append(c)
    return tasks


class CreateProjectItem(BaseModel):
    name: str = Field(..., description="The name can not be empty", min_length=1)
    description: str = Field(..., description="Description can not be empty", min_length=1)
    start_date: str = None
    end_date: str = None


@task_router.post('/project/create')
@valid_token
async def project_create(request: Request, task_info: CreateProjectItem):
    """ 创建项目 """
    if task_info.start_date is None:
        task_info.start_date = get_now().strftime('%Y-%m-%d')
    if task_info.end_date is None:
        task_info.end_date = get_now().strftime('%Y-%m-%d')
    task = mount(request, Task)
    # await task.find_one(name=task_info.name)
    # if task.id:
    #     raise EXIST_TASK
    task.leader = request.state.user.email
    task.priority = '正常'
    task.status = '进行中'
    await task.create(**task_info.dict())
    task.root = task.id
    await task.update_one(**task.data(not_none=True))
    return None


def ensure_task_admin_permission_single(request: Request, task: Task):
    if not ENABLE_PERMISSION_CHECK:
        return
    user = request.state.user.email
    if task.leader != user:
        raise PERMISSION_DENIED


# create/delete task
@task_router.get('/ensure/strict/admin/permission/{task_id}')
@valid_token
async def ensure_task_admin_permission_single_wrapper(request: Request, task_id: str):
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)
    ensure_task_admin_permission_single(request, task)
    return None


async def ensure_task_admin_permission(request: Request, task: Task):
    if not ENABLE_PERMISSION_CHECK:
        return
    user = request.state.user.email
    if task.leader == user:
        return
    if task.parent is None:
        raise PERMISSION_DENIED
    parent_task = mount(request, Task)
    await parent_task.from_id(task.parent)
    if parent_task.leader != user:
        raise PERMISSION_DENIED


# update task; add/remove participant
@task_router.get('/ensure/admin/permission/{task_id}')
@valid_token
async def ensure_task_admin_permission_wrapper(request: Request, task_id: str):
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)
    await ensure_task_admin_permission(request, task)
    return None


async def ensure_task_participation_permission(request: Request, task_id: str):
    if not ENABLE_PERMISSION_CHECK:
        return
    user = request.state.user.email
    participation = mount(request, Participation)
    await participation.find_one(user=user, task=task_id, flag=True)
    if participation.id:
        return
    task = mount(request, Task)
    await task.from_id(task_id)
    await ensure_task_admin_permission(request, task)


# download attachment; create comment
@task_router.get('/ensure/participation/permission/{task_id}')
@valid_token
async def ensure_task_participation_permission_wrapper(request: Request, task_id: str):
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)
    await ensure_task_participation_permission(request, task_id)
    return None


class CreateTaskItem(BaseModel):
    name: str = Field(..., description="The name can not be empty", min_length=1)
    leader: str = Field(..., description="Leader can not be empty", min_length=1)
    description: str = Field(..., description="Description can not be empty", min_length=1)
    start_date: str = None
    end_date: str = None
    root: str = None  # this field is ignored
    parent: str = Field(..., description="Parent can not be empty", min_length=1)
    position: int = 1


@task_router.post('/create')
@valid_token
async def create(request: Request, task_info: CreateTaskItem):
    """ 创建任务 """
    parent_task = mount(request, Task)
    # await parent_task.from_id(task_info.root, error=NOT_EXIST_TASK)
    await parent_task.from_id(task_info.parent, error=NOT_EXIST_TASK)

    ensure_task_admin_permission_single(request, parent_task)

    if task_info.start_date is None:
        task_info.start_date = get_now().strftime('%Y-%m-%d')
    if task_info.end_date is None:
        task_info.end_date = get_now().strftime('%Y-%m-%d')

    task_info.root = parent_task.root
    user = mount(request, User)
    await user.find_one(email=task_info.leader, to_raise=True, error=NOT_EXIST_USER)
    task = mount(request, Task)
    task.priority = '正常'
    task.status = '进行中'

    # adjust position
    query = FindQuery()
    query.filter = {'parent': parent_task.id}
    sibling_list = await parent_task.find(query)
    sibling_list = sibling_list['results']
    if len(sibling_list) == 0:
        await task.create(**task_info.dict())
        await parent_task.update_one(child=task.id)
        return None
    node_dict = {node['id']: node for node in sibling_list}
    if task_info.position < 1:
        task_info.position = 1
    if task_info.position > len(sibling_list) + 1:
        task_info.position = len(sibling_list) + 1
    child_ptr = parent_task.child
    if task_info.position == 1:
        await task.create(sibling=child_ptr, **task_info.dict())
        await parent_task.update_one(child=task.id)
        return None
    position = 2
    while position < task_info.position:
        child_ptr = node_dict[child_ptr]['sibling']
        position += 1
    if 'sibling' in node_dict[child_ptr]:
        await task.create(sibling=node_dict[child_ptr]['sibling'], **task_info.dict())
    else:
        await task.create(**task_info.dict())
    inserted_sibling_id = task.id
    await task.from_id(child_ptr)
    await task.update_one(sibling=inserted_sibling_id)
    return None


@task_router.post('/delete/{task_id}')
@valid_token
async def delete(request: Request, task_id: str):
    """ 删除任务 """
    current_task = mount(request, Task)
    await current_task.from_id(task_id, error=NOT_EXIST_TASK)

    if current_task.child is not None:
        raise EXIST_SUB_TASK

    parent_task = mount(request, Task)
    await parent_task.from_id(current_task.parent, error=NOT_EXIST_TASK)

    ensure_task_admin_permission_single(request, parent_task)
    
    # adjust position
    query = FindQuery()
    query.filter = {'parent': parent_task.id}
    sibling_list = await parent_task.find(query)
    sibling_list = sibling_list['results']
    assert len(sibling_list) > 0
    node_dict = {node['id']: node for node in sibling_list}
    child_ptr = parent_task.child
    if child_ptr == task_id:
        await parent_task.update_one(child=current_task.sibling, not_none=False)
        await current_task.update_one(sibling=None, parent=None, root=None, not_none=False)
        return None
    while node_dict[child_ptr]['sibling'] != task_id:
        child_ptr = node_dict[child_ptr]['sibling']
    print(child_ptr, current_task.sibling)
    task = mount(request, Task)
    await task.from_id(child_ptr)
    await task.update_one(sibling=current_task.sibling, not_none=False)
    await current_task.update_one(sibling=None, parent=None, root=None, not_none=False)
    return None


async def ensure_subtasks_finished(request: Request, task: Task):
    tasks = mount(request, Task)
    query = FindQuery()
    query.filter = {'parent': task.id}
    nodes = await tasks.find(query)
    nodes = nodes['results']
    node_dict = {node['id']: node for node in nodes}
    child_ptr = task.child
    while child_ptr is not None:
        if node_dict[child_ptr]['status'] != '已完成':
            raise EXIST_UNFINISHED_SUBTASK
        child_ptr = node_dict[child_ptr].get('sibling', None)


class UpdateTaskItem(BaseModel):
    id: str = None
    name: str = None
    description: str = None
    leader: str = None
    priority: str = None
    start_date: str = None
    end_date: str = None
    status: str = None


@task_router.post('/update')
@valid_token
async def update(request: Request, task_info: UpdateTaskItem):
    """ 更新任务/项目信息,任务之间的相对位置不能更改,更改状态时发送给上级审核 """
    current_task = mount(request, Task)
    await current_task.from_id(task_info.id, error=NOT_EXIST_TASK)

    await ensure_task_admin_permission(request, current_task)

    if task_info.leader is not None:
        user = mount(request, User)
        await user.find_one(email=task_info.leader, to_raise=True, error=NOT_EXIST_USER)
    task_info = task_info.dict(exclude_none=True)
    if 'status' in task_info and task_info['status'] != current_task.status:

        await ensure_subtasks_finished(request, current_task)

        if current_task.parent is None:
            # the only one who can modify the root is the project leader, 
            # so he can modify the status directly without any approval.
            if task_info['status'] == '已完成':
                pass
            elif task_info['status'] == '审核中':
                task_info['status'] = '已完成'
            else:
                raise INVALID_TASK_STATUS
        elif task_info['status'] == '审核中' and current_task.status == '进行中':
            if current_task.parent is not None:  # not root
                parent_task = mount(request, Task)
                await parent_task.from_id(current_task.parent)
                review = mount(request, Review)
                await review.create(
                    type=0,
                    task=current_task.id,
                    submitted_user=request.state.user.email,
                    submitted_datetime=get_now().strftime('%Y-%m-%d %H:%M'),
                    target_user=parent_task.leader
                )
        else:
            raise INVALID_TASK_STATUS
    await current_task.update_one(**task_info)
    return None


@task_router.post('/review/find/{mode}')
@valid_token
async def review_find(request: Request, find_query: FindQuery, mode: str):
    """ 查看当前用户的消息通知 """
    if mode == 'target':
        find_query.filter['target_user'] = request.state.user.email
        find_query.sort = [('submitted_datetime', -1)]
    else:
        find_query.filter['submitted_user'] = request.state.user.email
        find_query.sort = [('reply_datetime', -1)]
    reviews = mount(request, Review)
    lookup1 = LookUp(from_coll='user', from_field='submitted_user',
                     match_field='email', project={'name': 1, 'email': 1}, output_name='user_info')
    lookup2 = LookUp(from_coll='task', from_field='task',
                     match_field='_id', project={'name': 1, 'description': 1}, output_name='task_info')
    lookup3 = LookUp(from_coll='user', from_field='target_user',
                     match_field='email', project={'name': 1, 'email': 1}, output_name='target_user_info')
    return await reviews.find_with_aggregate(find_query, [lookup1, lookup2, lookup3])


@task_router.post('/review/update')
@valid_token
async def review_update(request: Request, review: Review):
    """ 更改当前用户的消息通知状态：status字段改为1或-1 """
    review.connect(request.app.state.mongo_client)
    data = review.data(not_none=True)
    await review.from_id(review.id, error=NOT_EXIST_REVIEW)
    if 'status' not in data:
        return None
    if data['status'] not in [-1, 1] or review.status != 0:
        raise INVALID_REVIEW_STATUS
    task = mount(request, Task)
    await task.from_id(review.task, error=NOT_EXIST_TASK)
    if data['status'] == -1:  # denied
        if review.type == 0:  # 0: approve task
            await task.update_one(status='进行中')
        elif review.type == 1:  # 1: task leader appointment
            pass
        elif review.type == 2:  # 2: task participant invitaion
            pass
    else:  # == 1, approved
        if review.type == 0:
            await task.update_one(
                status='已完成',
                end_date=get_now().strftime('%Y-%m-%d')
            )
        elif review.type == 1:
            pass
        elif review.type == 2:
            participation = mount(request, Participation)
            await participation.find_one(user=review.target_user, task=review.task)
            if participation.id:
                if not participation.flag:  # one can send the request for multiple times
                    await participation.update_one(flag=True)
            else:
                await participation.create(user=review.target_user, task=review.task)
    await review.update_one(
        status=data['status'],
        reply_datetime=get_now().strftime('%Y-%m-%d %H:%M')
    )
    return None


@task_router.post('/{task_id}/add/participant/{user_email}')
@valid_token
async def add_participant(request: Request, task_id: str, user_email: str):
    """ 添加执行人 """
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)

    await ensure_task_admin_permission(request, task)

    user = mount(request, User)
    await user.find_one(email=user_email, to_raise=True, error=NOT_EXIST_USER)
    participation = mount(request, Participation)
    await participation.find_one(user=user_email, task=task_id)
    if participation.id and participation.flag:
        raise EXIST_PARTICIPANT
    review = mount(request, Review)
    await review.create(
        type=2,
        task=task_id,
        submitted_user=request.state.user.email,
        submitted_datetime=get_now().strftime('%Y-%m-%d %H:%M'),
        target_user=user_email
    )
    return None


@task_router.post('/{task_id}/remove/participant/{user_email}')
@valid_token
async def remove_participant(request: Request, task_id: str, user_email: str):
    """ 删除执行人 """
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)

    await ensure_task_admin_permission(request, task)

    user = mount(request, User)
    await user.find_one(email=user_email, to_raise=True, error=NOT_EXIST_USER)
    participation = mount(request, Participation)
    await participation.find_one(user=user_email, task=task_id)
    if participation.id and participation.flag:
        await participation.update_one(flag=False)
    else:
        raise NOT_EXIST_PARTICIPANT
    return None


@task_router.get('/comment/find/{task_id}')
@valid_token
async def find_comments(request: Request, task_id: str):
    task = mount(request, Task)
    await task.from_id(task_id, error=NOT_EXIST_TASK)
    comments = mount(request, Comment)
    query = FindQuery()
    query.filter = {'task': task_id}
    lookup = LookUp(from_coll='user', from_field='user',
                    match_field='email', project={'name': 1, 'avatar': 1}, output_name='user_info')
    return await comments.find_with_aggregate(query, [lookup])


@task_router.get('/comment/download/{comment_id}')
@valid_token
async def download_attachment(request: Request, comment_id: str):
    comment = mount(request, Comment)
    await comment.from_id(comment_id, error=NOT_EXIST_COMMENT)

    await ensure_task_participation_permission(request, comment.task)

    storage = request.app.state.minio
    file = storage.get_object(bucket_name='commentfiles', object_name=comment.attachment)
    return StreamingResponse(
        content=file.stream(32*1024),
        headers={'Content-disposition': f"filename={quote(comment.attachment.split('/')[-1])}"},
        media_type='application/octet-stream'
    )


# class CreateCommentItem(BaseModel):
#     user: str = Field(..., description="User email can not be empty", min_length=1)
#     task: str = Field(..., description="Task can not be empty", min_length=1)
#     text: str = None


@task_router.post('/comment/create')
@valid_token
async def create_comment(request: Request, comment_info: str = Form(..., min_length=1), file: UploadFile = File(...)):
    """ 添加评论/执行记录 """
    comment_info = json.loads(comment_info)
    user = mount(request, User)
    await user.find_one(email=comment_info['user'], to_raise=True, error=NOT_EXIST_USER)
    task = mount(request, Task)
    await task.from_id(comment_info['task'], error=NOT_EXIST_TASK)

    await ensure_task_participation_permission(request, task.id)

    storage = request.app.state.minio
    # bucket_name不能包含下划线
    storage.create_bucket(bucket_name='commentfiles')
    suffix = gen_uuid()+'/'+file.filename
    content = await file.read()
    with io.BytesIO(content) as f:
        storage.put_object(bucket_name='commentfiles', object_name=suffix, data=f, length=len(content))

    comment = mount(request, Comment)
    await comment.create(
        attachment=suffix,
        datetime=get_now().strftime('%Y-%m-%d %H:%M'),
        **comment_info
    )

    return None





if __name__ == "__main__":
    pass
