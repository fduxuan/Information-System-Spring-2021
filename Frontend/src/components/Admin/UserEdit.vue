<!--
   Created on 2021/5/9 9:44 下午

   @Author: fduxuan

   Desc: 修改的表单
 */
 -->
<template>
    <div>
      <a-modal v-model="is_visible" :title="(mode==='Create' ? '创建':'修改') + '用户'"
               @cancel="handleCancel"
               @ok="handleOk"
               :confirm-loading="confirmLoading"
               >

        <a-form-model :model="user_edit" ref="user_edit_form" :rules="user_edit_rules">
          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 姓名 ---------------------->
            <a-form-model-item label="姓名" prop="name">
              <a-input style="width: 200px" v-model="user_edit.name" placeholder="输入真实姓名"></a-input>
            </a-form-model-item>

            <!----------------------- 性别 ---------------------->
            <a-form-model-item label="性别">
              <a-select style="width: 200px;"  v-model="user_edit.gender">
                <a-select-option value="male" >

                  <a-icon type="man" class="position-icon"/> 男
                </a-select-option>
                <a-select-option value="female">
                  <a-icon type="woman" class="position-icon"/> 女
                </a-select-option>
              </a-select>
            </a-form-model-item>
          </a-row>

          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 邮箱 ---------------------->
            <a-form-model-item label="邮箱" prop="email">
              <a-input style="width: 200px" v-model="user_edit.email" placeholder="输入真实邮箱" :disabled="disabled"></a-input>
            </a-form-model-item>

            <!----------------------- admin ---------------------->
            <a-form-model-item label="管理员权限" >
              <a-select style="width: 200px;"  v-model="user_edit.admin">
                <a-select-option value="false" >
                  否
                </a-select-option>
                <a-select-option value="true">
                  是
                </a-select-option>
              </a-select>

            </a-form-model-item>

            <!----------------------- 职位 ---------------------->
            <!-- <a-form-model-item label="Position" >
              <a-select style="width: 200px;"  v-model="user_edit.position">
                <a-select-option value="engineer" >
                  <a-icon type="team" class="position-icon"/> Engineer
                </a-select-option>
                <a-select-option value="customer">
                  <a-icon type="coffee" class="position-icon"/> Customer
                </a-select-option>
              </a-select>

            </a-form-model-item> -->
          </a-row>

          <a-row type="flex" align="middle" justify="space-around">
            <!----------------------- 地区 ---------------------->
            <!-- <a-form-model-item label="Region">
              <a-input style="width: 200px" v-model="user_edit.region" placeholder="Input Location"></a-input>
            </a-form-model-item> -->



          </a-row>
        </a-form-model>
      </a-modal>
    </div>

</template>

<script>
import UserService from "@/models/UserService";
export default {
    name: "UserEdit",
    components:{

    },
    props:{
      disabled: {
        type: Boolean,
        default() {return false}
      },
      visible: {
        type: Boolean,
        default() {return false}
      },
      info: {
        type: Object,
        default(){
          return {
            name: "",
            gender: "",
            email: "",
            position: "",
            admin: "",
            region: "",
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
          leader_name: undefined,
          user_edit: {
            name: "",
            gender: "male",
            email: "",
            region: "",
            admin: 'false',
            leader: ""
          },

          user_edit_rules: {
            name: [{ required: true, message: "姓名不可为空", trigger: 'blur' }],
            email:[{ required: true, message: "邮箱不可为空", trigger: 'blur' }],
          },
        }
    },

    methods:{
      /* 提交表单，校验 */
      async handleOk() {
        await this.$refs.user_edit_form.validate()
        let form = this.user_edit
        form.is_admin = this.user_edit.is_admin !== 'false'
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
        this.user_edit.gender = this.info.gender
        this.user_edit.email = this.info.email
        this.user_edit.position = this.info.position
        this.user_edit.admin = this.info.admin
        this.user_edit.region = this.info.region
      }

    },
    watch:{
      visible(newValue){
        this.is_visible = newValue
      },
      info(newValue){
        this.user_edit.name=newValue.name
        this.user_edit.gender = newValue.gender
        this.user_edit.email = newValue.email
        this.user_edit.position = newValue.position
        this.user_edit.admin = newValue.admin
        this.user_edit.region = newValue.region

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
