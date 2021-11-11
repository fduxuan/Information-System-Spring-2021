<!--
   Created on 2021/6/28 1:20 下午

   @Author: fduxuan

   Desc:  统计图表
 */
 -->
<template>
  <div>

    <a-row type="flex" align="middle">
      <!-------------------------- 总任务数目 --------------------------->
      <a-col :span="6">
        <a-card style="height: 220px">
          <h4>总任务数</h4>
          <span class="sub-title">所属项目: {{task_statistic.tasks[0].name}}</span>
          <a-statistic :value="task_statistic.tasks.length" suffix="个" :valueStyle="{fontSize: '36px', fontWeight: 'bold', color: '#1a2a67'}" style="text-align: center; margin-top: 40px;"/>
        </a-card>
      </a-col>

      <!-------------------------- 完成比例 --------------------------->
      <a-col :span="6">
        <a-card style="height: 220px">
          <h4>任务进度</h4>
          <span class="sub-title">所属项目: {{task_statistic.tasks[0].name}}</span>
          <ve-liquidfill style="text-align: center"   width="250px" height="150px"  :data="finish_task" :settings="finish_task_setting"></ve-liquidfill>
        </a-card>
      </a-col>

      <!-------------------------- 参与部门占比 --------------------------->
      <a-col :span="6">
        <a-card style="height: 220px">
          <h4>参与部门占比</h4>
          <span class="sub-title">所属项目: {{task_statistic.tasks[0].name}}</span>

          <ve-pie style="text-align: center" :legend-visible="false" width="250px" height="150px"  :data="department_user" :settings="department_user_setting"></ve-pie>

        </a-card>
      </a-col>

      <!-------------------------- 距离截止多少天 --------------------------->
      <a-col :span="6">
        <a-card style="height: 220px">
          <h4>距离『{{task_statistic.tasks[0].name}}』项目截止日期</h4>
          <span class="sub-title">{{end_date}}</span>
          <a-statistic :value="task_statistic.deadline" suffix="天" prefix="剩余" :valueStyle="{fontSize: '36px', fontWeight: 'bold', color: '#ee5a1f'}" style="text-align: center; margin-top: 40px;"/>
        </a-card>
      </a-col>

    </a-row>

    <a-divider></a-divider>
    <!-------------------------- 甘特图 --------------------------->

    <div>
      <div class="gstc-wrapper" ref="gstc"></div>
    </div>

  </div>

</template>

<script>
import moment from "moment";
import GSTC from 'gantt-schedule-timeline-calendar';
import { Plugin as TimelinePointer } from 'gantt-schedule-timeline-calendar/dist/plugins/timeline-pointer.esm.min.js';
import { Plugin as Selection } from 'gantt-schedule-timeline-calendar/dist/plugins/selection.esm.min.js';
import { Plugin as TimeBookmarks } from 'gantt-schedule-timeline-calendar/dist/plugins/time-bookmarks.esm.min.js';
import 'gantt-schedule-timeline-calendar/dist/style.css';
export default {
  name: "ProjectGraph",
  components: {},
  data() {
    return {
      end_date: "",
      finish_task: {
        columns: ['task', 'percent'],
        rows: [{
          task: '已完成',
          percent: 0.6
        }]
      },
      finish_task_setting:{
        seriesMap:{
          "已完成": {
            label: {
              fontSize: 25
            },
            radius: "70%",
            backgroudStyle: {
              color: "red",
            }
          }
        }
      },

      department_user:{
        columns: ['部门', '参与人数'],
        rows: [
          { '部门': '财务', '参与人数': 2 },
          { '部门': '质量', '参与人数': 3 },
          { '部门': '采购', '参与人数': 1 },
        ]
      },
      department_user_setting:{
        radius: 50,
        offsetY: 80,
        roseType: "radius",
      },

      sub_tasks: [],
      state: undefined,
      gstc: undefined,

      columns_gantt:{
        /* 名称 */
        'name' :{
          id: 'name',
          width: 200,
          data:'name',
          expander: true,
          header:{
            content: '名称'
          }
        },
        /* 负责人 */
        'leader': {
          id: 'leader',
          width: 160,
          data:'leaderInfo',
          header:{
            content: '负责人'
          },
          isHTML: true
        },
        /* 子任务完成度 */
        'progress': {
          id: 'progress',
          width: 100,
          data: 'progress',
          header: {
            content: '子任务进度'
          }
        },
        /* 是否已完成 */
        'status':{
          'id': 'status',
          width: 100,
          data: 'status',
          header: {
            content: '任务状态'
          },
          isHTML: true
        }
      },
      rows_gantt: {},
      items_gantt: {},
      bookmarks: {}
    }
  },
  props: {
    task_statistic:{
      type: Object,
      default(){return {}}
    }},

  methods: {

    processStatistic(){
      this.end_date = moment().add(this.task_statistic.deadline, "days").format("YYYY-MM-DD")
      this.finish_task = {
        columns: ['task', 'percent'],
        rows: [{
          task: '已完成',
          percent: this.task_statistic.finished / this.task_statistic.total
        }]
      }
      this.department_user = {
        columns: ['部门', '参与人数'],
        rows: [
          // { '部门': '财务', '参与人数': 2 },
          // { '部门': '质量', '参与人数': 3 },
          // { '部门': '采购', '参与人数': 1 },
        ]
      }
      for (let key in this.task_statistic.department_map){
        this.department_user.rows.push({'部门': key, '参与人数': this.task_statistic.department_map[key]})
      }
      if (this.task_statistic.unknow_departments > 0){
        this.department_user.rows.push({'部门': '未知', '参与人数': this.task_statistic.unknow_departments})
      }
    },

    /* 转换task对应格式 */
    generateRows(){
      // 随机颜色
      let colors = ['#96b2cd','#ab9be0','#ac8282',
        '#d0bb81','#9ed097','#9bd6cc'];
      let rows = {}
      let items = {}
      let tasks = this.task_statistic['tasks']
      tasks.forEach(t=>{
        t['parentId'] = this.task_statistic['pid'] === t['parentId'] ? undefined : t['parentId']
        t['leaderInfo'] =
            `<span class="task-info-user">` +
            `    <img src=${t["leader_info"]["avatar"]} style="width: 30px; border-radius: 50%">` +
            `    <span style="margin-left:5px">${t["leader_info"]["name"]}</span>`
        t['progress'] = `${t['finished']} / ${t['total']}`
        let statusColor = {
          background: 'rgba(0,127,191,0.1)',
          color: '#577085',
          border: '#d5e4da .02em solid'
        }
        if(t['status'] === '已完成'){
          statusColor = {
            background: 'rgb(0,191,10, 0.1)',
            color: '#299f09',
            border: '#d5e4da .02em solid'
          }
        }
        if(t['status'] === '审核中'){
          statusColor = {
            background: 'rgb(191,105,0, 0.1)',
            color: '#9f6809',
            border: '#d5e4da .02em solid'
          }
        }
        t['status'] = `<span style="border-radius: 4px;padding: 4px 8px 4px 8px; font-weight:bold; font-size: 12px;background: ${statusColor.background};color: ${statusColor.color}; border: ${statusColor.border}"> ${t['status']}</span>`
        rows[t['id']] = t
        items[t['id']] = {
          id: t['id'],
          label: `<span>` +
              `    <img src=${t["leader_info"]["avatar"]} style="width: 25px; border-radius: 50%">` +
              `    <span style="margin-left:5px">${t["leader_info"]["email"]}</span>`,
          rowId: t['id'],
          time: {
            start: t['start'],
            end: t['end'],
          },
          isHTML: true,
          style: {background: colors[Math.floor(Math.random()*colors.length)]},
          // height: 20
        }
        /* 增加截止符号 */
        items[t['id']+'_deadline'] = {
          id: t['id']+'_deadline',
          label: '<span style="background:#fff1f0 ;padding:0 5px 0 5px; border: 1px solid #ffa39e;color: #f5222d; font-size: 10px; font-weight: bold">预期</span>',
          rowId: t['id'],
          time:{
            start: GSTC.api.date(t['end_date']).startOf('day').valueOf(),
            end: GSTC.api.date(t['end_date']).endOf('day').valueOf(),
          },
          isHTML: true,
          style: {background: "#fff"}
        }
      })
      this.items_gantt = items
      this.rows_gantt = rows
    },

    /* 构建甘特图 */
    genGantt(){
      this.generateRows()
      const bookmarks = {
        'deadline': {
          // time: GSTC.api.date(this.task_statistic['end_date']).endOf('day').valueOf(),
          time:  GSTC.api.date().add(this.task_statistic['deadline'], 'day').valueOf(),
          color: '#db3442',
          label: '项目截止'
        }
      }
      const config = {
        licenseKey: "====BEGIN LICENSE KEY====\\nMZPgWJyGubpmCzYMM1ZNvy6aPpTedhTmnGPiQ/iivK3ZCmCB2blEVBAu/4117vGqNaohXWg0mSFXErCxuFVrJuD97929VhfX5auuEui9POCyIZ1nHbX+YbVaZN4ERrLiAPF8F8qs+Rg1M27IOFHkXz9vxevo4WN45dBqupdIVyIHvQttRymWDVbUJbvIGQUqiNrZH7tKSOJdAi2dwOi7hdRqT3B01PkKanRkSxNQ9nMrZziDFNMFZfkpQJ7nfdabFFtkvQf8c+wb0yFS4HU7PDwvkGpAiLUxbKP/3CU/v6CWKJ1mtL7OyQBa3Z7OGOopt6KMSLzqNWtqQaHhWz661w==||U2FsdGVkX1+RjZSIk0S+gBqCUJ88qentm6jxYmmvpT1UlHgjKJ+ys+XA1NQyyDNKvq1kE4FEWObMNLM29F6tKc9MLHvGb9VFzDT1onlyoYs=\\nsXP6ea/kEa9yDGNXggVNwO3hYH+XCIiwZrPIDEJT0TkId7Dxz/ZlAW2Auts9aF+W3PGydjlYEkz3qctAIU94ddkf46u+NUufHODIhwzu+1NuVUdY46rH3kKl5cWLysTBxMUn21OEp25oXPordcuM5X2R3ynF5ymo3EQfMh6P8rWWQZ75/xy9t2eK3U2yb2MbDOzGNDr2YEUXh3NyRTMJSoTt4w3EN455QgXMiedxS0M4EsFBATmXAWb/muzIyqFKz5tQkSZJszK6gacZdbrwBIkjc1NFQctw2M8rwfINvDrboMpmZqrvDkWbeSpujC4nod7eLaSok7j9QF6QIoPRQg==\\n====END LICENSE KEY====",
        plugins:[TimelinePointer(), Selection(), TimeBookmarks({bookmarks})],
        list:{
          columns:{data: this.columns_gantt},
          rows:this.rows_gantt,
        },
        chart:{
          items: this.items_gantt,
        }
      };
      let state = GSTC.api.stateFromConfig(config);
      this.gstc = GSTC({
        element: this.$refs.gstc,
        state,
      });
      this.state = state
    }

  },

  beforeUnmount() {
    if (this.gstc) this.gstc.destroy();
  },

  mounted() {
    console.log(this.task_statistic, 'tt')
    this.processStatistic()
    this.genGantt()
  },

  watch:{
    task_statistic(newValue){
      this.task_statistic = newValue
      this.genGantt()
    }
  }
}
</script>

<style scoped>

>>> .ant-card{
  box-shadow: 0 2px 2px 0 rgb(0 0 0 / 2%), 0 3px 1px -2px rgb(0 0 0 / 6%), 0 1px 5px 0 rgb(0 0 0 / 5%);
  margin: 8px;
}
>>> .ant-card-body{
  padding: 10px;
}
.sub-title{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  font-weight: bold;
  color: #918f8f;
  font-size: 70%;
}

>>> .ant-card:hover{
  box-shadow: 0 2px 2px 0 rgb(0 0 0 / 12%), 0 3px 1px -2px rgb(0 0 0 / 6%), 0 1px 5px 0 rgb(0 0 0 / 12%);
}

>>> .ant-statistic-content-prefix{
  font-size: 40%;
  color: #1a2a67
}

>>>.ant-statistic-content-suffix{
  font-size: 40%;
  color: #1a2a67
}

.gstc-component {
  margin: 0;
  padding: 0;
}
.toolbox{
  padding: 10px;
}

>>> span{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

>>>.task-info-user{
  background:rgba(9, 30, 66, 0.08); padding: 12px 10px; border-radius: 6px;
  align-items: center;
  /*display: inline-block;*/

}
>>>.task-info-user:hover{
  background:rgba(9, 30, 66, 0.18)
}
</style>
