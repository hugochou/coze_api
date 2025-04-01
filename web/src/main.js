import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import router from './router'
import pinia from './store'
import App from './App.vue'

// 导入自定义样式
import './assets/styles/index.css'

const app = createApp(App)

// 注册Element Plus
app.use(ElementPlus, {
  locale: zhCn, // 使用中文
  size: 'default'
})

// 注册Pinia
app.use(pinia)

// 注册路由
app.use(router)

// 错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('全局错误:', err)
  console.error('错误信息:', info)
}

// 挂载应用
app.mount('#app')
