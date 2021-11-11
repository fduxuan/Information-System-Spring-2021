<!--
   Created on 2021/7/6 1:15 下午

   @Author: fduxuan

   Desc: user 的图标
 */
 -->
<template>
  <a-tooltip>
    <template slot="title">
      {{user_info.email}}
    </template>
    <span :class="class_name">
      <a-avatar style="background-color:#87d068;" :src="user_info.avatar"/>
      <!-- todo: 这里应当展示用户名 -->
      <span style="margin-left:5px; top:3px; position: relative">{{user_info.name}}</span>
    </span>
  </a-tooltip>

</template>

<script>
export default {
    name: "UserIcon",
    components:{

    },
    data(){
        return{
          user_info:{
            name: "",
            avatar: "",
            id: "",
            email: ""
          },
          class_name: 'task-info-user'

        }
    },
    props: {
      user:{
        type: Object,
        default(){
          return {}
        }
      },
      type:{
        type: String,
        default(){
          return 'primary'
        }
      }

    },

    methods:{

    },

    mounted(){
      this.user_info = this.user
      if(this.type === 'text'){
        this.class_name = "task-info-user-text"
      }
    },

    watch:{
      user(newValue){
        this.user_info = newValue
      }
    }
}
</script>

<style scoped>

.task-info-user-text{
  align-items: center;
  display: inline-block;
}

.task-info-user{
  background: rgba(9, 30, 66, 0.08); padding: 8px 10px; border-radius: 6px;
  margin-right: 10px;
  align-items: center;
  display: inline-block;
}
.task-info-user:hover{
  background:rgba(9, 30, 66, 0.18)
}
</style>
