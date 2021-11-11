/*
 * Created on 2021/5/10 5:08 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */


import {Post, Get} from "./req"
// import axios from "axios";
import {message} from "ant-design-vue";

export default class TaskService {

    static async find_projects(find_query={}){
        return await Post('/api/task/project/find', find_query)
    }

    static async create_project(task_info){
        return await Post('/api/task/project/create', task_info)
    }

    static async project_info(project_id){
        return await Get(`/api/task/project/info/${project_id}`)
    }

    static async task_info(task_id){
        return await Get(`/api/task/info/${task_id}`)
    }

    static async createTask(create_form){
        return await Post('/api/task/create', create_form)
    }

    static async deleteTask(task_id){
        return await Post(`/api/task/delete/${task_id}`)
    }

    static async update(task){
        return await Post(`/api/task/update`, task)
    }

    static async add_participant(task_id, user_email){
        let res = await Post(`/api/task/${task_id}/add/participant/${user_email}`)
        message.success(`成功发送邀请通知，请等待对方确认!`)
        return res
    }

    static async remove_participant(task_id, user_email){
        let res = await Post(`/api/task/${task_id}/remove/participant/${user_email}`)
        message.success(`成功删除执行人!`)
        return res
    }

    static async getTaskInfo(task_id){
        return await Get(`/api/task/info/${task_id}`)
    }

    static async changeStatus(task_id, status){
        let res = await Post(`/api/task/update`, {id: task_id, status: status})
        message.success(`成功修改为${status}!`)
        return res
    }

    static async changeLeader(task_id, email){
        let res = await Post(`/api/task/update`, {id: task_id, leader: email})
        message.success(`成功修改责任人!`)
        return res
    }

    static async getTaskStatistic(project_id){
        return await Get(`/api/task/statistic/${project_id}`)
    }

    static async getProjectStatistic(project_id){
        return await Get(`/api/task/project/statistics/${project_id}`)
    }
    // static async update(department_info){
    //     return await Post(`/api/department/update`, department_info)
    // }

    // static async show(department_id){
    //     return await Get(`/api/department/show/${department_id}`)
    // }

    // static async invite(department_id, user_email) {
    //     return await Get(`/api/department/${department_id}/invite/${user_email}`)
    // }
}
