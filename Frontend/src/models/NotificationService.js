import {Post} from "./req"
// import axios from "axios";

export default class NotificationService {
    static async find(find_query={}, mode='target'){
        return await Post(`/api/task/review/find/${mode}`, find_query)
    }
    static async update(review){
        return await Post('/api/task/review/update', review)
    }
}
