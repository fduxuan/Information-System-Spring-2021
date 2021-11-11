import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: function () {
      return import('../views/Admin.vue')
    }
  },
  {
    path: '/profile/:uid',
    name: 'Profile',
    component: function () {
      return import('../views/UserProfile.vue')
    }
  },
  {
    path: '/department/:did',
    name: 'Department',
    component: function () {
      return import('../views/Department.vue')
    }
  },

  {
    path: '/project',
    name: '项目列表',
    component: function () {
      return import('../views/Project.vue')
    }
  },

  {
    path: '/projectDetail/:pid',
    name: '项目详情',
    component: function () {
      return import('../views/ProjectDetail.vue')
    }
  },

  {
    path: '/taskDetail/:tid',
    name: '任务详情',
    component: function () {
      return import('../views/TaskDetail.vue')
    }
  },

  {
    path: '/notification',
    name: '消息通知',
    component: function () {
      return import('../views/Notification.vue')
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

const defaultTitle = '项目管理|信息系统设计21'
router.beforeEach((to, from, next) => {
  document.title = to.name ? defaultTitle + ' | ' + to.name : defaultTitle
  next()
})


export default router
