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

export default class UserService {

    static async find(find_query={}){
        return await Post('/api/department/find', find_query)
    }

    static async create(department_info){
        let res = await Post('/api/department/create', department_info)
        message.success('创建部门成功！')
        return res
    }

    static async update(department_info){
        let res = await Post(`/api/department/update`, department_info)
        message.success('修改部门信息成功！')
        return res
    }

    static async show(department_id){
        return await Get(`/api/department/show/${department_id}`)
    }

    static async invite(department_id, user_email) {
        return await Get(`/api/department/${department_id}/invite/${user_email}`)
    }
}
