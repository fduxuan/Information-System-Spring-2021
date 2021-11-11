<!--
   Created on 2021/5/26 1:47 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
  <div style="padding: 20px 20px 40px 20px;">
    <a-card class="card-content">
      <h1> 我的个人信息 </h1>
      <a-divider></a-divider>
      <a-row>
        <a-col :span="6">
          <a-card >
            <!----------------------- 头像 ---------------------->

            <a-upload slot="cover" name="file" :fileList = "[]"
                      :showUploadList="false"
                      :beforeUpload="beforeUpload"
                      :customRequest="function(){}"
                      @change="handleChange"
            >
              <a-tooltip>
                <template slot="title">
                 点击修改头像
                </template>
                <img
                    style="width: 100%"
                    alt="/"
                    :src="user.avatar"
                />
              </a-tooltip>

            </a-upload>

            <!-- modal -->
            <CropperModal ref="CropperModal" @ok="handleCropperSuccess"></CropperModal>



            <!----------------------- 姓名/邮箱/职位 ---------------------->
            <a-card-meta>
              <template slot="description">
                <a-row style="font-size: 110%; font-weight: bold; color: #000;" type="flex" align="middle" justify="center">
                  {{user.name}}<a-icon type="man" style="margin-left:10px; font-size: 15px"/>
                </a-row>
                <a-divider style="margin-bottom: 10px"></a-divider>
                <a-row type="flex" align="middle"><a-icon type="mail"/>{{user.email}}</a-row>
                <a-divider v-if="department_info.name !== ''" style="margin: 10px 0 10px 0"></a-divider>
                <a-row v-if="department_info.name !== ''" type="flex" align="middle" ><a-icon type="flag" style=""/><a @click="$router.push({ path:`/department/${department_info.id}`}).catch(e=>{console.log(e)})">{{department_info.name}} ({{department_info.leader}})</a></a-row>
                <!-- <a-divider style="margin: 10px 0 10px 0"></a-divider>
                <a-row type="flex" align="middle" ><a-icon type="tag"/>{{user.position}}</a-row> -->
              </template>
            </a-card-meta>
          </a-card>
        </a-col>
        <a-col :span="17" :offset="1">
          <Relation :uid="$route.params.uid"></Relation>
        </a-col>
      </a-row>
    </a-card>
  </div>

</template>

<script>
import UserService from "@/models/UserService";
import DepartmentService from "@/models/DepartmentService";
import Relation from "@/components/UserProfile/Relation";
import CropperModal from "@/components/UserProfile/CropperModal";
export default {
    name: "UserProfile",
    components:{
      CropperModal,
      Relation
    },
    data(){
        return{
          uid: "",
          user: {
            id: "",
            position: ""
          },
          default_department_info: {
            id: "",
            name: "",
            leader: ""
          },
          department_info: {
            id: "",
            name: "",
            leader: ""
          },
          loading: false,
          imageUrl: ''
        }
    },
    props: {
    //图片格式
      imgFormat: {
        type: Array,
        default: function() {
          return ['image/jpeg']
        }
      },
      //图片大小
      imgSize: {
        type: Number,
        default: 2
      },
      //图片裁切配置
      options: {
        type: Object,
        default: function() {
          return {
            autoCropWidth: 300,
            autoCropHeight: 300
          }
        }
      },
      //回显图片路径
      value: {
        type: String,
        default: ''
      }
    },

    methods:{
      //从本地选择文件
      handleChange(info) {
        let { options } = this
        this.getBase64(info.file.originFileObj, (imageUrl) => {
          let target = Object.assign({}, options, {
            img: imageUrl
          })
          this.$refs.CropperModal.edit(target)
        })
      },
      // 上传之前 格式与大小校验
      beforeUpload(file) {

        let fileType = file.type
        if (fileType.indexOf('image') < 0) {
          this.$message.warning('Please Upload File')
          return false
        }
      },
      //裁剪成功后的File对象
      async handleCropperSuccess(data) {
        const formData = new FormData()
        formData.append('user_id', this.user.id)
        formData.append('file', data.file)
        console.log(formData.get('user_id'))
        await UserService.changeAvatar(formData)
        this.user.avatar=data.data
        this.$message.success("Change successfully!")



      },

      getBase64(img, callback) {
        const reader = new FileReader()
        reader.addEventListener('load', () => callback(reader.result))
        reader.readAsDataURL(img)
      },

      /* 获取个人信息 或者其他人信息 */
      async info(){

        this.user = await UserService.show(this.uid)

        if (this.user.department) {
          this.department_info = await DepartmentService.show(this.user.department);
        } else {
          this.department_info = this.default_department_info;
        }
      }
    },

    async mounted(){

      this.uid = this.$route.params.uid
      await this.info()
    },

    watch: {
      value: {
        handler(val) {
          this.imageUrl = val || ''
        },
        immediate: true
      },
      async '$route' (to, from) { //监听路由是否变化
        if(to.params.uid !== from.params.uid){
          this.uid = to.params.uid;
          await this.info()
        }
      }

    },

}
</script>

<style scoped>
.card-content{
  text-align: left;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  box-shadow:-1px 1px 3px #ACADA3;
}

>>> .anticon{
  margin-right: 20px; color:#000
}

>>>.ant-upload.ant-upload-select{
  display: block;
  cursor: pointer;
}

</style>
