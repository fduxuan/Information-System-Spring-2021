/*
 * Created on 2021/5/10 5:08 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */


import {Post, Get} from "./req"
import axios from "axios";
// import {message} from "ant-design-vue";

export default class CommentService {

    static async find_comments(task_id){
        return await Get(`/api/task/comment/find/${task_id}`)
    }

    static async download_comment(comment_id){
        const config = {
            headers: {
            'Content-Type': 'application/octet-stream'
            },
            responseType: 'arraybuffer',
        }
        return await axios.get(`/api/task/comment/download/${comment_id}`, config)
    }

    static async create_comment(form_data){
        const headers = {
            'Content-Type': 'multipart/form-data',
        }
        return await Post('/api/task/comment/create', form_data, headers)
    }

    

    // static async add_participant(task_id, user_email){
    //     let res = await Post(`/api/task/${task_id}/add/participant/${user_email}`)
    //     message.success(`成功添加执行人!`)
    //     return res
    // }

    // static async remove_participant(task_id, user_email){
    //     let res = await Post(`/api/task/${task_id}/remove/participant/${user_email}`)
    //     message.success(`成功删除执行人!`)
    //     return res
    // }

    // static async getTaskInfo(task_id){
    //     return await Get(`/api/task/info/${task_id}`)
    // }

    // static async changeStatus(task_id, status){
    //     let res = await Post(`/api/task/update`, {id: task_id, status: status})
    //     message.success(`成功修改为${status}!`)
    //     return res
    // }

    // static async changeLeader(task_id, email){
    //     let res = await Post(`/api/task/update`, {id: task_id, leader: email})
    //     message.success(`成功修改责任人!`)
    //     return res
    // }

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
