<template>
    <div style="padding: 20px 20px 40px 20px;">
      <a-card class="card-content">
        <h2>我的通知</h2>
        <a-divider />

        <a-row type="flex" align="top">
          <a-col span="4" >
            <a-menu mode="inline"
              :open-keys="openKeys"
              @openChange="onOpenChange"
              @click="handleMenuClick"
              style="text-align: left;border-radius: 10px; "
              v-model="current_menu"
            >
              <!---------------------- 系统消息 -------------------->
              <a-menu-item :key="10" class="menu-font">
                <a-icon type="setting" />
                系统通知
              </a-menu-item>

              <!---------------------- 收到的项目参与邀请 -------------------->
              <a-sub-menu key="sub1">
                <span slot="title"><a-icon type="sound" /><span class="menu-font">&nbsp;邀请我参与</span></span>
                <a-menu-item :key="item.key" class="menu-font" v-for="item in subMenu">
                  {{ item.value }}
                </a-menu-item>
              </a-sub-menu>

              <!---------------------- 收到的审批请求 -------------------->
              <a-sub-menu key="sub2">
                <span slot="title"><a-icon type="notification" /><span class="menu-font">&nbsp;请求我审批</span></span>
                <a-menu-item :key="item.key+3" class="menu-font" v-for="item in subMenu">
                  {{ item.value }}
                </a-menu-item>
              </a-sub-menu>


            </a-menu>

          </a-col>

          <a-col :span="19" :offset="1">
            <div class="notification-list">
              <a-spin :spinning="spinning">
                <!---------------------- 使用三个component来控制三种类型的通知 -------------------->
                <ReceiveInvitation keep-alive :notifications="notifications.slice(pageSize*current-pageSize, Math.min(pageSize*current, notifications.length))"
                                    v-if="current_mode===1" @handleNotiChange="handleNotiChange"></ReceiveInvitation>
                <ReceiveApproval :notifications="notifications.slice(pageSize*current-pageSize, Math.min(pageSize*current, notifications.length))"
                                  v-else-if="current_mode===2" @handleNotiChange="handleNotiChange"></ReceiveApproval>
                <SystemNotification :notifications="notifications.slice(pageSize*current-pageSize, Math.min(pageSize*current, notifications.length))"
                                    v-if="current_mode===3" @handleNotiChange="handleNotiChange"></SystemNotification>
                <br>

                <!---------------------- 分页 -------------------->
                <div v-if="notifications.length !== 0" style="text-align: right">
                  <a-pagination v-model="current"
                                :total="notifications.length"
                                :pageSize="pageSize"
                                @change="changePage"
                                show-less-items />
                </div>
                
              </a-spin>
            </div>



          </a-col>
        </a-row>
      </a-card>
    </div>

</template>

<script>
// import InvitationService from "@/models/InvitationService";
import NotificationService from "@/models/NotificationService";
import ReceiveInvitation from "@/components/Notification/ReceiveInvitation";
import ReceiveApproval from "@/components/Notification/ReceiveApproval";
import SystemNotification from "@/components/Notification/SystemNotification";
export default {
    name: "Notification",
    components:{
      ReceiveInvitation,
      ReceiveApproval,
      SystemNotification
    },
    data(){
        return{
          subMenu:[
            {key: 1, value: '未操作'},
            {key: 2, value: '接受'},
            {key: 3, value: '拒绝'},
          ],
          openKeys: ['sub1', 'sub2'],
          notifications: [],
          current: 1,
          pageSize: 3,
          current_menu: [10],
          spinning: false,
          current_status: "unread",
          current_mode: 3
        }
    },

    methods:{

      /* menu最上层开关 */
      onOpenChange(openKeys) {
        this.openKeys = openKeys
      },

      /* 分页 */
      changePage(current){
        this.current = current
      },

      /* 根据menu选择拉取不同数据 */
      async handleMenuClick(doc){
        this.current = 1
        this.current_status = [1, 4].includes(doc.key) ? 'init': this.current_status         // 是否为未操作
        this.current_status = [2, 5].includes(doc.key) ? 'accept': this.current_status       // 是否为已接受
        this.current_status = [3, 6].includes(doc.key) ? 'reject': this.current_status       // 是否为已拒绝
        this.current_status = doc.key === 10 ? 'unread': this.current_status                 // 是否为未读
        // this.current_status = doc.key === 11 ? 'read': this.current_status                   // 是否为已读

        this.current_mode = [1, 2, 3].includes(doc.key) ? 1: this.current_mode    // 是否是拉取接受消息
        this.current_mode = [4, 5, 6].includes(doc.key) ? 2: this.current_mode    // 是否是拉取发送消息
        this.current_mode = [10, 11].includes(doc.key) ? 3: this.current_mode     // 是否是拉取系统消息

        await this.getNotifications()
      },

      /* 拉取信息的函数 */
      async getNotifications(){
        this.spinning = true
        if(this.current_mode === 1){ // 拉取收到的参与任务邀请
          let status = 0;
          if (this.current_status === 'accept') status = 1;
          else if (this.current_status === 'reject') status = -1;
          this.notifications = await NotificationService.find({filter: {status: status, type: 2}});
          this.notifications = this.notifications.results;
        }
        else if (this.current_mode === 2){ // 拉取收到的任务完成审批邀请
          let status = 0;
          if (this.current_status === 'accept') status = 1;
          else if (this.current_status === 'reject') status = -1;
          this.notifications = await NotificationService.find({filter: {status: status, type: 0}});
          this.notifications = this.notifications.results;
        }
        else{ // 拉取系统消息
          this.notifications = await NotificationService.find({filter: {status: -1}}, 'submitted');
          this.notifications = this.notifications.results;
        }
        this.spinning = false
      },

      handleNotiChange(index) {
        this.notifications.splice(index, 1)
      }

    },

    mounted(){
      this.getNotifications()
    },
}
</script>

<style scoped>

.card-content{
  text-align: left;
  padding: 0px 15px;
  -moz-box-shadow:-1px 1px 3px #ACADA3;
  -webkit-box-shadow:-1px 1px 3px #ACADA3;
  box-shadow:-1px 1px 3px #ACADA3;
}

.menu-font {
  font-size: 110%;
}

</style>