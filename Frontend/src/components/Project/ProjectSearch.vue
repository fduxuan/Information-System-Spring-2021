<!--
   Created on 2021/6/6 7:07 下午

   @Author: fduxuan

   Desc:
 */
 -->
<template>
    <div>
      <h2>我的项目</h2>
      <br>
      <a-row type="flex" align="middle">
        <!-------------------------- 是否为负责人筛选 --------------------------->
        <a-select default-value="all" style="width: 120px" @change="handleFilterChange" v-model="filter_type">
          <a-select-option value="all">我的参与</a-select-option>
          <a-select-option value="leader">
            我的负责
          </a-select-option>
        </a-select>

        <!-------------------------- 是否已完成筛选 --------------------------->
        <a-select default-value="all" style="width: 120px; margin-left: 20px" @change="handleFilterChange" v-model="filter_finished_type">
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="finished">
            已完成
          </a-select-option>
          <a-select-option value="unfinished">
            未完成
          </a-select-option>
        </a-select>

        <!-------------------------- 项目名称 --------------------------->
        <a-input v-model="searchProjectName"  style="width: 200px; margin-left: 20px; margin-right: 20px"></a-input>

        <a-tooltip title="搜索">
          <a-button type="primary" shape="circle" icon="search" @click="handleClickSearch()"  style="background: #8db2c3; border-color: #8db2c3; margin-right: 20px"/>
        </a-tooltip>
        <a-tooltip title="重置">
          <a-button type="primary" shape="circle" icon="delete" @click="handleClickReset()" style="background: #8db2c3; border-color: #8db2c3"/>
        </a-tooltip>

        <a-button type="primary" style="margin-left: auto; font-weight: bold" shape="round" @click="visible=true">新建项目</a-button>
      </a-row>

      <a-modal
          title="创建新项目"
          :visible="visible"
          :confirm-loading="confirmLoading"
          @ok="createProject"
          @cancel="handleCancel"
      >
        <ProjectCreate @change="getForm"></ProjectCreate>
      </a-modal>
    </div>

</template>

<script>
import ProjectCreate from "@/components/Project/ProjectCreate";
import TaskService from "@/models/TaskService";
export default {
    name: "ProjectSearch",
    components:{
      ProjectCreate

    },
    data(){
        return{
          ModalText: 'Content of the modal',
          visible: false,
          confirmLoading: false,
          create_form: {name: '', start_date: '', end_date: '', description: ''},
          searchProjectName: '',
          filter_type: 'all',
          filter_finished_type: 'all',
        }
    },
    props: {

    },

    methods:{
      /* 创建项目 */
      async createProject() {
        if(this.create_form.name === ''){this.$message.error('请填写项目名称！'); return}
        if(this.create_form.description === ''){this.$message.error('请填写项目详细信息！');return}
        if(this.create_form.start_date === '' || this.create_form.end_date === ''){this.$message.error('请填写项目时间！');return}

        this.confirmLoading = true;
        await TaskService.create_project(this.create_form);
        setTimeout(() => {
          this.handleCancel();
          this.$emit("handleProjectCreated");
        }, 2000);
      },
      handleCancel() {
        this.visible = false;
        this.confirmLoading = false;
      },

      getForm(form){
        this.create_form = form
      },

      handleFilterChange(value){
        console.log(value)
        let filter = {
          'type': this.filter_type,
          'finished_type': this.filter_finished_type,
          'projectName': this.searchProjectName
        }
        this.$emit('handleFilterChange', filter)
      },

      handleClickSearch(){
        console.log(this.searchProjectName)
        let filter = {
          'type': this.filter_type,
          'finished_type': this.filter_finished_type,
          'projectName': this.searchProjectName
        }
        this.$emit('handleFilterChange', filter)
      },

      handleClickReset(){
        this.filter_type = 'all';
        this.filter_finished_type = 'all';
        this.searchProjectName = '';
        let filter = {
          'type': this.filter_type,
          'finished_type': this.filter_finished_type,
          'projectName': this.searchProjectName
        }
        this.$emit('handleFilterChange', filter)
      }
    },

    mounted(){

    },
}
</script>

<style scoped>

</style>
