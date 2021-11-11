# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 11:09 上午

@Author: fduxuan

Desc:

"""
from itertools import count as _count


class ApiException(Exception):

    uni_name = "ApiException"  # 用户使用api可能遇到的错误码

    def __init__(self, code, reason=None):
        self.code = code
        self.reason = reason

    def dict(self, **kwargs):
        result = {
            "code": self.code,
            "data": self.reason
        }
        result.update(kwargs)
        return result

    def __call__(self, *, code=None, reason=None):
        return type(self)(code or self.code, reason or self.reason)

    def __str__(self):
        return f'Code: {self.code}, reason: {self.reason}'


""" 异常表 """
error_count = _count()

NORMAL = ApiException(next(error_count), 'normal')
UNKNOWN_ERROR = ApiException(next(error_count), '未知错误')
NO_PRIVILEGE = ApiException(next(error_count), "权限不足")

""" 用户相关 """
NOT_LOGIN = ApiException(next(error_count), '未登录')
NOT_EXIST_USER = ApiException(next(error_count), '用户不存在')
EXIST_USER = ApiException(next(error_count), '用户已存在')
LOGIN_ERROR = ApiException(next(error_count), 'Email或密码错误')
NOT_ADMIN = ApiException(next(error_count), '非管理员')
EXIST_EMAIL = ApiException(next(error_count), 'Email已存在')
EMAIL_FORMAT_ERROR = ApiException(next(error_count), 'Email格式不正确')

"""  关系 """
DUPLICATE_RELATION = ApiException(next(error_count), 'The two users already have a relationship')

""" Minio """
UPLOAD_ERROR = ApiException(next(error_count), '上传过程中出现错误，请重试')
DOWNLOAD_ERROR = ApiException(next(error_count), '下载过程中出现错误，请重试')
REMOVE_ERROR = ApiException(next(error_count), '删除过程中出现错误，请重试')


""" 业务相关 """
MONTH_FORMAT_ERROR = ApiException(next(error_count), '年月格式为：YYYY-MM')
DATE_FORMAT_ERROR = ApiException(next(error_count), '日期格式为：YYYY-MM-DD')
EXIST_PROCESSING_DAILY = ApiException(next(error_count), 'You still have a form in progress')
NOT_EXIST_DAILY = ApiException(next(error_count), 'There is no such form')

""" Department-Related """
EXIST_DEPARTMENT = ApiException(next(error_count), '部门已存在')
NOT_EXIST_DEPARTMENT = ApiException(next(error_count), '部门不存在')
INVITE_DEPARTMENT_LEADER = ApiException(next(error_count), '不能邀请部门经理')

PERMISSION_DENIED = ApiException(next(error_count), '请求被拒绝：权限错误！')

"""
Task Related
"""
EXIST_TASK = ApiException(next(error_count), '任务已存在')
NOT_EXIST_TASK = ApiException(next(error_count), '任务不存在')

EXIST_SUB_TASK = ApiException(next(error_count), '该任务包含子任务')

NOT_EXIST_PROJECT = ApiException(next(error_count), '项目不存在')

NOT_EXIST_REVIEW = ApiException(next(error_count), '请求不存在')
INVALID_REVIEW_STATUS = ApiException(next(error_count), '状态不合法')

EXIST_PARTICIPANT = ApiException(next(error_count), '执行人已存在')
NOT_EXIST_PARTICIPANT = ApiException(next(error_count), '执行人不存在')

NOT_EXIST_COMMENT = ApiException(next(error_count), '执行记录不存在')

INVALID_TASK_STATUS = ApiException(next(error_count), '任务状态不合法')
EXIST_UNFINISHED_SUBTASK = ApiException(next(error_count), '该任务包含未完成的子任务')


if __name__ == "__main__":
    pass
