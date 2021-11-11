/*
 * Created on 2021/5/10 5:08 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */


import {Post, Get} from "./req"
import axios from "axios";
import {message} from "ant-design-vue";


export default class UserService {

    static async login(data) {
        let res =  await Post(`/api/user/login`, data)
        message.success('登录成功！')
        return res
    }

    static async info(){
        const config = {
            headers: {'Content-Type': 'application/json;charset=UTF-8'},
            params: {}
        }
        const resp = await axios.get(`/api/user/info`, config)
        const data = resp.data
        if (resp.status !== 200) {
            throw resp.statusText
        }
        if (data.code !== 0) {
            throw data.error
        }
        return data.data
    }

    static async logout(){
        let res = await Post(`/api/user/logout`)
        message.success('注销成功!')
        return res
    }

    static async find(find_query={}){
        return await Post('/api/user/find', find_query)
    }

    static async create(user_info){
        return await Post('/api/user/create', user_info)
    }

    static async update(user_info){
        return await Post(`/api/user/update`, user_info)
    }

    static async resetPassword(user_id){
        return await Post(`/api/user/reset/${user_id}`)
    }

    static async show(user_id){
        return await Get(`/api/user/show/${user_id}`)
    }

    static async changeAvatar(formData){
        const headers = {
            'Content-Type': 'multipart/form-data',
        }
        return await Post('/api/user/change/avatar', formData, {headers: headers})
    }
}
