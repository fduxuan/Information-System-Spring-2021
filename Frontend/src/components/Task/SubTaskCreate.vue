<template>
  <a-modal
    :title="this.modalTitle"
    okText="提交"
    cancelText="取消"
    :visible="visible"
    :confirm-loading="confirmLoading"
    @ok="handleOk"
    @cancel="handleCancel">
    <div>

    <a-form-model
      ref="createTaskForm"
      :rules="formRules"
      :model="form"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 12 }" >
      <a-form-model-item label="名称:" prop="name">
        <a-input
          v-model="form.name"
          placeholder="请输入任务名称"
        />
      </a-form-model-item>

      <a-form-model-item label="优先级:" prop="priority">
        <a-select :value="form.priority" placeholder="请选择任务优先级" @change="handlePriorityChange">
          <a-select-option value="高优">高优</a-select-option>
          <a-select-option value="中优">中优</a-select-option>
          <a-select-option value="正常">正常</a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item label="开始时间:" prop="start_date">
        <a-date-picker
          v-model="form.start_date"
          placeholder="请选择任务开始时间"
          :disabledDate="startTimeDisable"
        />
      </a-form-model-item>
      <a-form-model-item label="结束时间:" prop="end_date">
        <a-date-picker
          v-model="form.end_date"
          placeholder="请选择任务结束时间"
          :disabledDate="endTimeDisable"
        />
      </a-form-model-item>

      <a-form-model-item label="描述:" prop="description">
        <a-textarea
            v-model="form.description"
            placeholder="请输入任务描述"
            :auto-size="{ minRows: 3, maxRows: 20 }"
        />
      </a-form-model-item>
      <a-form-model-item label="负责人:" prop="leader">
        <a-input
          v-model="form.leader"
          placeholder="请输入任务负责人邮箱"
        />
          <!-- <a-select
            v-model="form.leader"
            show-search
            optionFilterProp="label"
            placeholder="选择负责人"
          >
          <a-select-option v-for="user in users" :key="user.id" :value="user.id" :label="user.name">
              {{ user.name }}
            </a-select-option>
          </a-select> -->
      </a-form-model-item>
      <!-- <a-form-model-item label="执行人:" prop="executor">
        <a-select
            mode="multiple"
            v-model="form.executor"
            show-search
            optionFilterProp="label"
            placeholder="选择执行人"
        >
            <a-select-option v-for="user in users" :key="user.id" :value="user.id" :label="user.name">
                {{ user.name }}
            </a-select-option>
            
        </a-select>
      </a-form-model-item> -->

      <!-- <a-form-model-item label="任务附件:" prop="fileList">
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
      </a-form-model-item> -->
    </a-form-model>
    </div>
  </a-modal>
</template>

<script>
import moment from "moment"
const formRules = {
  name: [{ required: true, message: '请输入任务名称!', trigger: 'blur' }],
  priority: [{ required: true, message: '请输入任务优先级!', trigger: 'blur'}],
  leader: [{ required: true, message: '请输入任务负责人邮箱!', trigger: 'blur' }],
  // start_date: [{ required: true, message: '请选择任务开始时间!', trigger: 'blur' }],
  // end_date: [{ required: true, message: '请选择任务结束时间!', trigger: 'blur' }],
  description: [{ required: true, message: '请输入任务描述!', trigger: 'blur' }],
  // executor: [{ type: 'array', required: true, message: '请选择任务执行人!', trigger: 'blur' }],
}


export default {
  name: "SubTaskCreate",
  props: {
    visible: {
      type: Boolean,
      default() {return false}
    },
    confirmLoading: {
      type: Boolean,
      default() {return false}
    },
    modalType: { // 后续可用于modal复用
    },
    modalTitle: {},
    modalForm: {},
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
      form: this.modalForm,
      // fileList: [],
      // uploadFile: undefined,
    }
  },
  methods: {
    handlePriorityChange (priority) {
      this.form = {
        ...this.form,
        priority,
      }
    },
    handleOk() {
      this.$refs.createTaskForm.validate(validate => {
        if (validate) {
          // if (this.modalType == 'create' && this.uploadFile === undefined){
          //   this.$message.error('no file attached!')
          // }
          // else{
              let formData = this.form
              // formData['uploadFile'] = this.uploadFile
              // console.log(formData.uploadFile)
              // console.log('submission form', formData)
              this.$emit('handleClickOk', formData)
              // this.fileList = []
              // this.uploadFile = undefined
          // }
        }
      });
    },
    handleCancel() {
      this.$emit('handleClickCancel')
      // this.fileList = []
      // this.uploadFile = undefined
    },

    // 上传/预览文件操作
    /*究极魔改只接受一个file*/
    // async handleUploadFile(info){
    //   // 仅保留一个
    //   if (info.file.type !== 'application/pdf'){
    //     this.$message.error('You can only upload PDF file!');
    //     return
    //   }
    //   this.fileList = [info.file]
    //   this.uploadFile = info
    //   console.log(this.uploadFile)

    // },

    // remove(){
    //   this.fileList = []
    //   this.uploadFile = undefined
    // },

    // async handleClickPreview() {
    //   console.log(this.currentDraft);
    //   const fid = this.currentDraft.file_id
    //   const pdfURL = this.$router.resolve({path: `/pdfpreview/${fid}`})
    //   window.open(pdfURL.href, '_blank')
    // },


     // 时间验证
    startTimeDisable(current){
      let disabled = false
      if (current < moment().endOf('day').subtract(1, 'day')){  // 必须是今天之后的日期
        disabled = true
      }
      if (this.form.end_date && current > moment(this.form.end_date.endOf('day'))){  // 必须早于结束时间
        disabled = true
      }
      return disabled
    },


    endTimeDisable(current){
      let disabled = false
      if (current < moment().endOf('day').subtract(1, 'day')){  // 必须是今天之后的日期
        disabled = true
      }
      if (this.form.start_date && current < moment(this.form.start_date.endOf('day')).subtract(1, 'day')){ // 必须晚于开始时间
        disabled = true
      }
      return disabled
    },

    
  },
  mounted() {
  },
  watch:{
    modalForm(newValue,oldValue){
      console.log(oldValue, newValue)
      this.form = newValue
    },

  }
}
</script>

<style scoped>

</style>