<template>
  <a-list item-layout="vertical" :data-source="notifications">
    <a-list-item slot="renderItem" slot-scope="item, index" class="no-border-list">
      <!-------------------- 标题为 来自xxx（任务负责人）的审批请求，关于xxx任务 ------------------->
      <a-card class="notification-card"
              :headStyle="headStyle"
              v-if="item.user_info"
              :title="'来自 '+item.user_info[0].name+' 关于 【'+item.task_info[0].name+'】 的审批请求'">
        <span slot="extra" style="font-size: 50%">{{ item.submitted_datetime }}</span>
        <a-row>
          <!-------------------- 左三分之一为请求者（任务负责人）信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">任务负责人信息</p>
            <p>姓名: {{item.user_info[0].name}}</p>
            <p>Email: {{item.user_info[0].email}}</p>
          </a-col>
          <!-------------------- 中三分之一为任务信息 ------------------->
          <a-col :span="8">
            <p class="notification-title">
                任务信息
                <a-tooltip placement="top">
                    <template slot="title">
                    <span>详情</span>
                    </template>
                    <a-icon type="info-circle" style="font-size: 20px; cursor:pointer; margin-right: 10px;" @click="$router.push({ path:`/taskDetail/${item.task_info[0]._id}`}).catch(e=>{console.log(e)})" />
                </a-tooltip>
            </p>
            <p>名称: {{item.task_info[0].name}}</p>
            <p>内容: {{item.task_info[0].description}}</p>
          </a-col>
          <!-------------------- 右三分之一为操作 ------------------->
          <a-col :span="7" :offset="1">
            <p class="notification-title">操作</p>
            <br>

            <a-row v-if="item.status===0">
              <a-col :span="6">
                <a-popconfirm
                    title="你确定要审核通过该请求吗？" ok-text="确认" cancel-text="取消"
                    @confirm="approve_invitation(item._id, index)">
                  <!-------------------- 接受 ------------------->
                  <a-button class="notification-button" type="primary">通过</a-button>
                </a-popconfirm>
              </a-col>
              <a-col :span="6">
                <a-popconfirm
                    title="你确定要拒绝通过该请求吗？" ok-text="确认" cancel-text="取消"
                    @confirm="reject_invitation(item._id, index)">
                  <!-------------------- 拒绝 ------------------->
                  <a-button class="notification-button" type="danger">拒绝</a-button>
                </a-popconfirm>
              </a-col>
            </a-row>

            <!-------------------- 已经操作的invitation ------------------->
            <a-row v-else>
              <a-button :disabled="true" class="notification-button">{{get_status(item.status)}}</a-button>
            </a-row>
          </a-col>

        </a-row>
      </a-card>
    </a-list-item>
  </a-list>
</template>

<script>
import NotificationService from "@/models/NotificationService";
export default {
    name: "ReceiveApproval",
    components:{

    },
    props: {
      notifications: {
        type: Array,
        default() {return []}
      }
    },
    data(){
        return{
          headStyle: { fontSize: "150%", color: "#060930", backgroundColor: 'rgba(234, 240, 241, 0.7)' }
        }
    },

    methods:{
      get_status(status) {
        if (status === 1) return '已通过';
        else if (status === -1) return '已拒绝';
        return undefined;
      },
      /* 接受邀请 */
      async approve_invitation(iid, index){
        await NotificationService.update({
          id: iid,
          status: 1
        });
        this.$message.success('通过审批！')
        this.$emit('handleNotiChange', index)
      },

      /* 拒绝邀请 */
      async reject_invitation(iid, index){
        await NotificationService.update({
          id: iid,
          status: -1
        });
        this.$message.success('拒绝审批！')
        this.$emit('handleNotiChange', index)
      }

    }
  }
</script>

<style scoped>

.notification-card{
  border-radius: 4px;
  text-align: left;
}

.notification-title{
  font-weight: bold;
  font-size: 110%;
  color:#16697a;
}
.notification-button{
  font-weight: bold;
}

.ant-list-split .no-border-list.ant-list-item {
  border-bottom: none;
}
</style>
