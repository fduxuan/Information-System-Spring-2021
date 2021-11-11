<!--
   Created on 2021/5/28 12:54 下午

   @Author: fduxuan

   Desc: 个人为中心的关系图
 */
 -->
<template>
  <div>
    <!----------------------- 个人关系图 -------------------->
    <div style="width: 100%;height:calc(100vh); border: 1px solid #e8e8e8">
      <SeeksRelationGraph ref="seeksRelationGraph" :options="userGraphOptions">
        <div slot="node" slot-scope="{node}">
          <a-dropdown>
          <div class="c-my-node" :style="{border: '#5dbce0 solid 3px', cursor: 'pointer', 'background-image': `url(${node.data.avatar})`}">
            <div class="c-node-name" style="color:#02334c">{{node.data.name}}</div>
          </div>
            <!-- <a-menu slot="overlay" class="node-option-nav" v-if="$store.state.user.admin">
              <a-menu-item v-if="uid === node.id && user.position === 'engineer'" @click="handleOptions(node,options[0])">Change Superior</a-menu-item>
              <a-menu-item v-if="uid === node.id && user.position === 'engineer'" @click="handleOptions(node,options[1])">Adding Subordinate</a-menu-item>
              <a-menu-item v-if="uid === node.id && user.position === 'engineer'" @click="handleOptions(node,options[2])">Adding Customers</a-menu-item>
              <a-menu-item v-if="uid === node.id && user.position === 'customer'" @click="handleOptions(node,options[3])">Adding Supporters</a-menu-item>
                <a-menu-item v-if="uid !== node.id">
                  <a-popconfirm
                      title="Are you sure delete this relation?"
                      ok-text="Yes"
                      cancel-text="No"
                      @confirm="confirm(node.id)"
                  >Delete
                  </a-popconfirm>
                </a-menu-item>

            </a-menu> -->
          </a-dropdown>
        </div>
      </SeeksRelationGraph>

      <!-- <a-modal v-model="visible" :title="option" @ok="createRelation" :confirm-loading="confirm_loading">
        <UserSelect @change="searchUser" :value="search_name" :extra_query="extra_query"></UserSelect>
      </a-modal> -->
    </div>


  </div>

</template>

<script>
import SeeksRelationGraph from 'relation-graph'
import RelationService from "@/models/RelationService";
import UserService from "@/models/UserService";
// import UserSelect from "@/components/Admin/UserSelect";

export default {
  name: "Relation",
  // components: {SeeksRelationGraph, UserSelect},
  components: {SeeksRelationGraph},
  props: {
    uid: {type: String},
  },

  data() {
    return {
      relations: [],
      user: {},
      option: "Change Superior",
      options: ["Change Superior", 'Adding Subordinates', "Adding Customers","Adding Supporters", 'Delete'],
      visible: false,
      confirm_loading: false,
      search_name: undefined,
      search_uid: undefined,
      extra_query: {},
      userGraphOptions: {
        defaultNodeBorderWidth: 0,
        defaultNodeColor: 'rgba(238, 178, 94, 1)',
        allowSwitchLineShape: true,
        allowSwitchJunctionPoint: true,
        defaultLineShape: 1,
        'layouts': [
          {
            'label': '中心',
            'layoutName': 'center',
            'layoutClassName': 'seeks-layout-center',
          }
        ],
      }

    }
  },


  methods: {
    /* 打开选择用户 */
    handleOptions(node, option){
      this.option = option
      this.extra_query = this.option === this.options[2] ? {position: 'customer'} : {position: 'engineer'}
      this.visible = true
      // console.log(node, option)
    },

    /* 搜索特定用户 */
    // async searchUser(data){
    //   this.search_name = data.name
    //   this.search_uid = data.uid
    // },

    /* 删除对应关系 */
    // async confirm(uid){
    //   console.log(uid)
    //   await RelationService.delete({from_uid: this.uid, to_uid: uid})
    //   await RelationService.delete({from_uid: uid, to_uid: this.uid})
    //   await this.setGraphData()
    //   this.$message.success("Delete Successfully")
    // },

    /* 创建关系 */
    // async createRelation(){
    //   this.confirm_loading = true
    //   try{
    //     if(this.option === this.options[0]){
    //       // 修改领导
    //       await RelationService.delete({to_uid: this.uid, ship: 'leadership'})
    //       await RelationService.create(({from_uid: this.search_uid, to_uid: this.uid, ship: 'leadership'}))
    //     }
    //     else if (this.option === this.options[1]){
    //       // 增加下级
    //       await RelationService.create({from_uid: this.uid, to_uid: this.search_uid, ship: 'leadership'})
    //     }
    //     else if (this.option === this.options[2]){
    //       // 增加客户
    //       await RelationService.create({from_uid: this.uid, to_uid: this.search_uid, ship: 'supporting'})
    //     }
    //     else{
    //       // 增加支持
    //       await RelationService.create({from_uid: this.search_uid, to_uid: this.uid, ship: 'supporting'})
    //     }
    //     await this.setGraphData()
    //   }finally {
    //     setTimeout(() => {
    //       this.visible = false;
    //       this.confirm_loading = false;
    //       this.$message.success('Change Successfully!')
    //     }, 1500);
    //   }
    // },


    /* 获取用户关系 */
    async getRelation(){
      // let query = {'$or': [{'from_uid': this.uid}, {'to_uid': this.uid}]}
      let res = await RelationService.find(this.uid)
      this.relations = res['results']
    },

    /* 将用户转化为节点的格式 */
    userToNode(user_id, user_name, user_avatar){
      return {
        id: user_id, nodeShape: 0,
        data: {name: user_name, avatar: user_avatar},
        innerHTML: `<div class="c-my-node"
                   style="background-image: url(${user_avatar});
                   border:#5dbce0 solid 3px;">
                   <div class="c-node-name" style="color:#02334c">${user_name}</div>
                   </div>`
      }
    },
    departmentToNode(user_id, user_name){
      return {
        id: user_id, nodeShape: 0,
        data: {name: user_name, avatar: "https://minio.droproblem.com/avatar2/logo_black.png"},
        innerHTML: `<div class="c-my-node"
                   style="border: #5dbce0 solid 3px;">
                   <div class="c-node-name" style="color:#02334c">${user_name}</div>
                   </div>`
      }
    },

    async setGraphData() {
      let graphData = {
        rootId: this.uid,
        nodes: [],
        links: []
      }
      // 添加用户和关系
      graphData.nodes.push(this.userToNode(this.uid, this.user.name, this.user.avatar))
      await this.getRelation()
      this.relations.forEach(r=>{

        graphData.nodes.push(this.departmentToNode(r.from_info.id, r.from_info.name))
        graphData.nodes.push(this.userToNode(r.to_info.id, r.to_info.name, r.to_info.avatar))
        // 保存有关系的节点
        r.lineWidth = 2

        if(r.from_info.leader === r.to_info.email){
          r.from = r.to_info.id
          r.to = r.from_info.id

          r.text = "部门领导"
          r.color = "#3d9ae7"
          r.lineWidth = 4
          // if(r.from_uid === this.uid){
          //   r.text = 'Your Subordinate'
          //   r.color = "#6a3de7"
          // }
        }
        else{
          r.from = r.from_info.id
          r.to = r.to_info.id

          // r.text = ''
          r.color = "#1bca6f"
        }
        graphData.links.push(r)
      })
      this.$refs.seeksRelationGraph.setJsonData(graphData, () => {
      })
    }
  },

  async mounted() {
    this.user = await UserService.show(this.uid)
    await this.setGraphData()
  },

  watch:{
    async uid(newValue){
      this.user = await UserService.show(newValue)
      await this.setGraphData()
    }
  }


}
</script>

<style scoped>
>>>.c-my-node{
  background-position: center center;
  background-size: 100%;
  border:#ff8c00 solid 2px;
  height:80px;
  width:80px;
  border-radius: 40px;
}

>>>.c-node-name{
  width:160px;margin-left:-40px;text-align:center;margin-top:85px; font-weight: bold;
}

>>> .c-node-text{
  font-weight: bold;
  font-size: 110%;
}

>>> .ant-btn {
  font-weight: bold;
  background: rgb(141, 178, 195);
  border-color: rgb(141, 178, 195);
  color: #fff

}

>>>.c-rg-link-text{
  font-weight: bold;
  font-size: 12px;
}

>>>.ant-dropdown-menu-item{
  align-items: center;
  font-size: 90%;
}

.node-option-nav{
  position: relative;
  left: 70px;
  top: -30px;
  color: #eaeaea;
  background: #edf4f6;
  padding: 1px 0 1px 0;
  border-radius: 3px;
}

</style>
