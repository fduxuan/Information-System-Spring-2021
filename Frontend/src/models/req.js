/*
 * Created on 2021/5/10 5:07 下午
 *
 * @Author: fduxuan
 *
 * Desc:
 */


import axios from "axios"
import { message } from 'ant-design-vue'

export async function Get(url, config=undefined, disable_message_error=false) {

    if(config === undefined) {config = {}}
    if(config.params === undefined) {config.params = {}}
    config.headers = {'Content-Type': 'application/json;charset=UTF-8'}
    let resp = await axios.get(url, config);
    let data = resp.data;
    if(resp.status !== 200) {
        throw resp.statusText
    }
    if(data.code !== 0) {
        console.log(data)
        if (!disable_message_error){
            message.error(data.data)
        }
        throw data.data
    }
    return data.data
}

export async function Post(url, data, config=undefined, disable_message_error=false) {
    if(config === undefined) {config = {}}
    if (config.headers === undefined) {
        config['headers'] = {'Content-Type': 'application/json;charset=UTF-8'}
    }
    config.withCredentials=true
    let resp = await axios.post(url, data, config)

    let respData = resp.data
    if(resp.status !== 200) {
        throw resp.statusText
    }
    if(respData.code !== 0) {
        if (!disable_message_error){
            message.error(respData.data)
        }
        throw respData.data
    }
    return respData.data
}
