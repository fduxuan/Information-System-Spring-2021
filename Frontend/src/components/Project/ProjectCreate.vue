<!--
   Created on 2021/6/7 6:32 下午

   @Author: fduxuan

   Desc: 创建表单
 */
 -->
<template>
    <div>
      <a-row type="flex" align="middle" style="margin-bottom: 30px">
        <span class="project-create-title">项目名称:</span>
        <a-input style="width:280px" placeholder="填写项目名称" v-model="create_form.name" @change="change"></a-input>
      </a-row>

      <a-row type="flex" align="middle" style="margin-bottom: 30px">
        <span class="project-create-title">项目时间:</span>
        <a-range-picker @change="onChange"  style="width: 280px"/>
      </a-row>

      <a-row type="flex" align="middle">
        <span class="project-create-title">项目信息:</span>
        <a-textarea
            v-model="create_form.description"
            @change="change"
            placeholder="项目详细描述信息"
            style="width: 330px"
            :auto-size="{ minRows: 7, maxRows: 10 }"
        />
      </a-row>

    </div>

</template>

<script>
export default {
    name: "ProjectCreate",
    components:{

    },
    data(){
        return{
          ModalText: 'Content of the modal',
          create_form: {
            name: '',
            start_date: '',
            end_date: '',
            description: ''
          }
        }
    },
    props: {
    },

    methods:{
      onChange(date, dateString) {
        this.create_form.start_date = dateString[0]
        this.create_form.end_date = dateString[1]
        this.change()
      },

      change(){
        this.$emit('change', this.create_form)
      }
    },

    mounted(){

    },


}
</script>

<style scoped>
.project-create-title{
  font-weight: bold; margin-right: 30px; font-size: 15px
}
</style>
