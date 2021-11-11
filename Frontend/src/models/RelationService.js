/*
 * Created on 2021/5/24 3:23 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */
import {Get} from "./req"


export default class RelationService {

    // static async create(data) {
    //     return await Post(`/api/relation/create`, data)
    // }

    // static async find(find_query={}){
    //     return await Post('/api/relation/find', find_query)
    // }
    static async find(uid){
        return await Get(`/api/relation/find/${uid}`)
    }

    // static async delete(query = {}){
    //     return await Post('/api/relation/delete', {filter: query})
    // }
}
