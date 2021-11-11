<!--
   Created on 2021/5/9 9:44 下午

   @Author: fduxuan

   Desc: 修改的表单
 */
 -->
<template>
    <div>
      <a-modal v-model="is_visible" :title="(mode==='Create'? '创建': '修改')+ '部门'"
               @cancel="handleCancel"
               @ok="handleOk"
               :confirm-loading="confirmLoading"
               >

        <a-form-model :model="user_edit" ref="user_edit_form" :rules="user_edit_rules">
          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 部门名 ---------------------->
            <a-form-model-item label="部门名称" prop="name">
              <a-input style="width: 200px" v-model="user_edit.name" placeholder="请输入部门名称"></a-input>
            </a-form-model-item>
          </a-row>

          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 领导邮箱 ---------------------->
            <a-form-model-item label="部门领导" prop="leader">
              <UserSelect @change="(e)=>{user_edit.leader=e.email}"></UserSelect>
            </a-form-model-item>
          </a-row>

          <!-- <a-row type="flex" align="middle" justify="space-around"> -->

            <!----------------------- admin ---------------------->
            <!-- <a-form-model-item label="Is Admin" >
              <a-select style="width: 200px;"  v-model="user_edit.admin">
                <a-select-option value="false" >
                  False
                </a-select-option>
                <a-select-option value="true">
                  True
                </a-select-option>
              </a-select>

            </a-form-model-item> -->

          <!-- </a-row> -->
        </a-form-model>
      </a-modal>
    </div>

</template>

<script>
import UserService from "@/models/UserService";
import UserSelect from "@/components/Admin/UserSelect";
export default {
    name: "DepartmentEdit",
    components:{
      UserSelect

    },
    props:{
      visible: {
        type: Boolean,
        default() {return false}
      },
      info: {
        type: Object,
        default(){
          return {
            name: "",
            email: ""
          }
        }
      },
      mode: {
        type: String,
        default(){return 'Create'}
      },

      confirmLoading: {
        type: Boolean,
        default(){return false}
      }
    },

    data(){
        return{
          is_visible: false,
          fetching: false,
          users: [],
          user_edit: {
            name: "",
            leader: ""
          },

          user_edit_rules: {
            name: [{ required: true, message: "名称不可为空", trigger: 'blur' }],
            // email:[{ required: true, message: "Email cannot be empty", trigger: 'blur' }],
          },
        }
    },

    methods:{
      /* 提交表单，校验 */
      async handleOk() {
        await this.$refs.user_edit_form.validate()
        let form = this.user_edit
        this.$emit('submit',form)
      },

      /* 删除表单内容和校验 */
      handleCancel(){
        this.$refs.user_edit_form.resetFields()
        this.$emit('cancel')
      },

      /* 获取数据 */
      async fetchUser(value){
        this.fetching = true;
        if(!['', undefined].includes(value)){
          try{
            let res = await UserService.find({filter: {'name': {'$regex': value}}, limit: 20})
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


    },

    mounted(){
      this.is_visible=this.visible
      if (this.mode === 'Edit'){
        this.user_edit.name=this.info.name
        this.user_edit.leader = this.info.leader
      }

    },
    watch:{
      visible(newValue){
        this.is_visible = newValue
      },
      info(newValue){
        this.user_edit.name=newValue.name
        this.user_edit.leader = newValue.leader

      }
    }
}
</script>

<style scoped>
.position-icon{
  font-size: 110%;
  font-weight: bold;
  margin-right: 5px;
}
</style>
