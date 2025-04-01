import { createRouter, createWebHistory } from 'vue-router'

// 导入视图组件
// 使用懒加载方式导入组件，优化首次加载性能
const Home = () => import('../views/Home.vue')
const Upload = () => import('../views/Upload.vue')
const Videos = () => import('../views/Videos.vue')
const Creator = () => import('../views/Creator.vue')
const ApiTest = () => import('../views/ApiTest.vue')

// 定义路由
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload,
    meta: {
      title: '上传管理'
    }
  },
  {
    path: '/videos',
    name: 'Videos',
    component: Videos,
    meta: {
      title: '视频管理'
    }
  },
  {
    path: '/creator',
    name: 'Creator',
    component: Creator,
    meta: {
      title: '视频创建'
    }
  },
  {
    path: '/api-test',
    name: 'ApiTest',
    component: ApiTest,
    meta: {
      title: 'API测试'
    }
  },
  // 默认重定向到首页
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫，动态设置标题
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '首页'} - Coze API`
  next()
})

export default router 