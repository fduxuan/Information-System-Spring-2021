# -*- coding: utf-8 -*-
"""
Created on 2021/5/4 1:36 下午

@Author: fduxuan

Desc:

"""
from .helper import *
from error import *
import os


PROJECT_ROOT = os.path.dirname(os.path.abspath('__file__'))

test_db = TestDb()
api_user = MyClient('/api/user')


def test_login():
    test_db.user.drop()
    res = api_user.post('/login')
    assert res.code != 0
    # 不存在用户
    res = api_user.post('/login', {'email': '123@qq.com', 'password': 'ddd'})
    assert res.code == LOGIN_ERROR.code

    test_db.fake_user(_id='id', email='123@qq.com', password='ddd')
    res = api_user.post('/login', {'email': '123@qq.com', 'password': 'ddd'})
    assert res.code == 0
    assert 'set-cookie' in res.headers


def test_info():
    test_db.user.drop()
    test_db.redis_clear()
    res = api_user.get('/info')
    assert res.code == NOT_LOGIN.code

    test_db.fake_admin_login_user()
    res = api_user.get('/info')
    assert res.code == 0
    assert res.data['name'] == 'admin'


def test_find():
    test_db.user.drop()
    test_db.fake_admin_login_user()
    res = api_user.post('/find')
    assert res.data['count'] == 1

    test_db.fake_user(_id='t', name='小明', leader='login_admin_user')
    res = api_user.post('/find')
    assert res.data['count'] == 2

    res = api_user.post('/find', {'filter': {'name': "小明"}})
    assert res.data['count'] == 1


def test_create():
    test_db.user.drop()
    test_db.fake_admin_login_user()
    res = api_user.post('/find')
    assert res.data['count'] == 1
    # 完整性
    res = api_user.post('/create', {'name': 'adf'})
    assert res.code != 0
    # 邮箱格式
    res = api_user.post('/create', {'name': 'adf', 'email': 'xx'})
    assert res.code == EMAIL_FORMAT_ERROR.code
    # 正常
    res = api_user.post('/create', {'name': '1', 'email': 'test@qq.com'})
    assert res.code == 0
    res = api_user.post('/find')
    assert res.data['count'] == 2

    # 重复邮箱
    res = api_user.post('/create', {'name': '1', 'email': 'test@qq.com'})
    assert res.code == EXIST_EMAIL.code

    # 初始化密码为邮箱
    res = api_user.post('/login', {'email': 'test@qq.com', 'password': 'test@qq.com'})
    assert res.code == 0


def test_admin_update():
    test_db.user.drop()
    test_db.fake_admin_login_user()
    test_db.fake_user(_id='id', email='123@qq.com', password='ddd', name='小明')
    # 没有传id
    res = api_user.post('/update', {"email": '12@qq.com'})
    assert res.code != 0

    res = api_user.post('/update', {'id': 'id', 'email': '12@qq.com', 'name': '小红'})
    assert res.code == 0
    assert res.data['email'] == '12@qq.com'
    assert res.data['name'] == '小红'


def test_reset_password():
    test_db.user.drop()
    test_db.fake_admin_login_user()
    test_db.fake_user(_id='id', email='123@qq.com', password='ddd', name='小明')
    # 无此id
    res = api_user.post('/reset/fake')
    assert res.code != 0
    # 正常
    res = api_user.post('/reset/id')
    assert res.code == 0
    res = api_user.post('/login', {'email': '123@qq.com', 'password': '123@qq.com'})
    assert res.code == 0


def test_show_user():
    test_db.user.drop()
    test_db.fake_ordinary_login_user()
    test_db.fake_user(_id='ddd', name='小明', password='123')

    res = api_user.get('/show/ddd')
    assert res.code == 0
    assert res.data['name'] == '小明'
    assert 'password' not in res.data


def test_avatar():
    test_db.fake_ordinary_login_user()
    f = open(f'{PROJECT_ROOT}/tests/test_avatar.jpg', 'rb')
    res = api_user.post('/change/avatar', form={'user_id': 'login_ordinary_user'}, files={'file': f})
    assert res.code == 0
    assert res.data['avatar'] is not None

    res = api_user.post('/change/avatar', form={'user_id': 'ddd'}, files={'file': f})
    assert res.code == NO_PRIVILEGE.code



if __name__ == "__main__":
    pass
