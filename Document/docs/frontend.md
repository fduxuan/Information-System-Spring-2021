# 页面设计

<img src="https://img.shields.io/badge/Vue-AntD-informational" />

* `展示地址`: [http://106.14.244.24:8080](http://106.14.244.24:8080)
* `测试账号`：账号 admin@qq.com  密码 admin123



## 首页

* `登录与注销` 

* `登录前不可访问任何业务页面`

   	![](https://minio.droproblem.com/document/page/home-logout.png)

   	![](https://minio.droproblem.com/document/page/home-login.png)



----

## 系统管理页面

* ### 权限控制页面

   	如果用户为管理员，则头部显示系统管理；如果非管理员，则不显示，并且访问对应路径会显示错误

  非管理员通过路径访问报错：

  ![](https://minio.droproblem.com/document/page/not-admin.png)

  ​	  	

  

* ### 用户管理页面

   	管理员可进行 `添加用户` `修改用户信息`  `重置用户密码` `筛选与搜索`

  

    ![](https://minio.droproblem.com/document/page/admin-user.png)

  

    ![](https://minio.droproblem.com/document/page/admin-useredit.png)

  



* ### 部门管理页面

   	和用户管理相同，管理员可进行`部门创建` `修改部门基本信息` `增加部门成员` `部门搜索筛选`等等

   	![](https://minio.droproblem.com/document/page/admin-department.png)

    ![](https://minio.droproblem.com/document/page/admin-department-info.png)



----

## 项目页面

* ### 项目首页

    `仅能查看自己参与的项目` `项目的搜索与筛选`

    ![](https://minio.droproblem.com/document/page/project-list.png)

* ### 项目详情页面

    `WBS任务树` `看板` `任务信息`

    ![](https://minio.droproblem.com/document/page/project-detail.png)

    ![](https://minio.droproblem.com/document/page/kanban.png)



* ### 项目数据统计页面

    `总任务统计` `进度统计`  `参与部门占比`  `截止日期` `甘特图`

    ![](https://minio.droproblem.com/document/page/graph.png)

    ![](https://minio.droproblem.com/document/page/gantt.png)

   

---



## 任务页面

* ### 任务详情

    `编辑任务` `添加子任务` `添加执行记录` `上传下载附件` `完成任务` `邀请执行人`

     ![](https://minio.droproblem.com/document/page/task.png)



---

## 通知页面

`系统通知 ` `邀请参与` `请求审批`

![](https://minio.droproblem.com/document/page/notification.png)



-----

## 个人信息页

`上传头像` `部门用户关系`

![](https://minio.droproblem.com/document/page/profile.png)

![](https://minio.droproblem.com/document/page/avatar.png)



-----

## 权限错误提示

非任务负责人（或父任务负责人）修改任务信息提示权限错误

![](https://minio.droproblem.com/document/page/permission-denied.png)
