/*
 * Created on 2021/5/10 5:08 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */


import {Get} from "./req"
// import axios from "axios";
// import {message} from "ant-design-vue";

export default class PermissionService {

    static async is_strict_leader(task_id){
        try{
            await Get(`/api/task/ensure/strict/admin/permission/${task_id}`, undefined, true)
        }catch(error){
            return false
        }
        return true       
    }

    static async is_leader(task_id){
        try{
            await Get(`/api/task/ensure/admin/permission/${task_id}`, undefined, true)
        }catch(error){
            return false
        }
        return true       
    }

    static async is_participant(task_id){
        try{
            await Get(`/api/task/ensure/participation/permission/${task_id}`, undefined, true)
        }catch(error){
            return false
        }
        return true
    }

}
