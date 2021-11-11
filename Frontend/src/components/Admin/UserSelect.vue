<!--
   Created on 2021/5/24 10:38 上午

   @Author: fduxuan

   Desc:  搜索user的select
 */
 -->
<template>
    <div>
      <a-select
          show-search
          :value="name"
          placeholder="输入用户姓名或者邮箱"
          style="width: 200px"
          :show-arrow="false"
          :filter-option="false"
          :not-found-content="fetching ? undefined : null"
          @search="fetchUser"
          @change="handleChange"
      >
        <a-spin v-if="fetching" slot="notFoundContent" size="small" />
        <a-select-option v-for="(d, index) in users" :key="index" :label="d.name">
          <div style="overflow-x: auto; display: flex; align-items: center">
            <a-avatar style="background-color:#87d068; margin-right: 8px" icon="user" />
            <div style="font-size: 80%">
              <p style="font-weight: bold; margin: 0">{{d.name}}</p>
              <p style="color: grey; margin: 0">{{d.email}}</p>
            </div>
          </div>
        </a-select-option>

      </a-select>
    </div>

</template>

<script>
import UserService from "@/models/UserService";

export default {
    name: "UserSelect",
    components:{

    },
    data(){
        return{
          name: undefined,
          fetching: 'false',
          users: [],
          uid: '',
        }
    },
    props: {
      value: {
        type: String,
        default(){return undefined}
      },
      extra_query: {
        type: Object,
        default() {
          return {};
        }
      }
    },

    methods:{
      /* 获取数据 */
      async fetchUser(value){
        if(!['', undefined].includes(value)){
          this.fetching = true;
          try{
            let query = {"$or": [{'name': {'$regex': value}}, {'email': {'$regex': value}}]}
            if(this.extra_query !== {}){
              query = {"$and": [query, this.extra_query]}
            }
            let res = await UserService.find({filter: query, limit: 20})
            this.users = res['results']
          }finally {
            this.fetching = false
          }
        }
        else{
          this.users = []
          this.fetching = false
        }
      },

      handleChange(index) {
        this.name = this.users[index]['name']
        this.uid = this.users[index]['id']
        this.$emit('change', {'name': this.name, 'uid': this.uid, 'email': this.users[index]['email']})
      }
    },

    mounted(){
      this.name = this.search_name
    },

    watch:{
      value(newValue){
        this.name = newValue
      }
    }
}
</script>

<style scoped>

</style>
