<template>
  <a-modal
    title="新建任务执行记录"
    okText="提交"
    cancelText="取消"
    :visible="visible"
    :confirm-loading="confirmLoading"
    @ok="handleOk"
    @cancel="handleCancel">
    <div>

    <a-form-model
      ref="executionRecordForm"
      :rules="formRules"
      :model="form"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 12 }" >
      <!-- <a-form-model-item label="执行状态:" prop="state">
        <a-input
          v-model="form.state"
          placeholder="请输入任务执行状态"
        />
      </a-form-model-item> -->

      <a-form-model-item label="执行记录描述:" prop="description">
        <a-textarea
            v-model="form.description"
            placeholder="请输入任务执行记录描述"
            :auto-size="{ minRows: 3, maxRows: 20 }"
        />
      </a-form-model-item>

      <a-form-model-item label="执行记录附件:" prop="fileList">
          <div class="dropbox">
          <a-upload-dragger
              name="file"
              :customRequest="handleUploadFile"
              :file-list="fileList"
              :remove="remove"

          >
            <p class="ant-upload-drag-icon">
              <a-icon type="inbox" />
            </p>
            <p class="ant-upload-text">
              点击或拖动文件到该区域上传
            </p>
            <p class="ant-upload-hint">
              只能提交一个文件，若有多个文件请打包
            </p>
          </a-upload-dragger>
        </div>
      </a-form-model-item>
    </a-form-model>
    </div>
  </a-modal>
</template>

<script>
const formRules = {
  description: [{ required: true, message: '请输入任务执行记录描述!', trigger: 'blur' }],
}


export default {
  name: "ExecutionRecord",
  props: {
    visible: {
      type: Boolean,
      default() {return false}
    },
    confirmLoading: {
      type: Boolean,
      default() {return false}
    },
    // users: {
    //   default() {
    //     return [
    //       {"id": 1, "name": "Jie Shi", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"},
    //       {"id": 2, "name": "Xuanjie Fang", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"}, 
    //       {"id": 3, "name": "Yanqi Jiang", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"},
    //       {"id": 4, "name": "Yiwen Xu", "avatar": "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"}
    //       ]
    //   }
    // }
  },
  data() {
    return {
      formRules,
      form: {},
      fileList: [],
      uploadFile: undefined,
    }
  },
  methods: {
    handleOk() {
      this.$refs.executionRecordForm.validate(validate => {
        if (validate) {
            if (this.uploadFile == undefined){
                this.$message.error("请上传一个附件！")
                return
            }
            let formData = this.form
            formData['file'] = this.uploadFile
            console.log('submission form', formData)
            this.$emit('handleClickOk', formData)
            this.fileList = []
            this.uploadFile = undefined
            // this.form.description = ""
        }
      });
    },
    handleCancel() {
      this.$emit('handleClickCancel')
      this.fileList = []
      this.uploadFile = undefined
    },

    // 上传/预览文件操作
    /*究极魔改只接受一个file*/
    async handleUploadFile(info){
      // 仅保留一个
    //   if (info.file.type !== 'application/pdf'){
    //     this.$message.error('You can only upload PDF file!');
    //     return
    //   }
      this.fileList = [info.file]
      this.uploadFile = info
      console.log(this.uploadFile)

    },

    remove(){
      this.fileList = []
      this.uploadFile = undefined
    },

    // async handleClickPreview() {
    //   console.log(this.currentDraft);
    //   const fid = this.currentDraft.file_id
    //   const pdfURL = this.$router.resolve({path: `/pdfpreview/${fid}`})
    //   window.open(pdfURL.href, '_blank')
    // },

    
  },
  mounted() {
  },
  watch:{
    modalForm(newValue,oldValue){
      console.log(oldValue)
      this.form = newValue
    },

  }
}
</script>

<style scoped>

</style>