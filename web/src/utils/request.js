import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  // API基础URL，从环境变量中读取，默认为本地开发地址
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  // 请求超时时间
  timeout: 30000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    // 例如：添加请求头、添加认证信息等
    
    // 添加请求标识
    config.headers['X-Requested-With'] = 'XMLHttpRequest'
    
    // TODO: 添加认证Token（如果有）
    // const token = getToken()
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`
    // }
    
    return config
  },
  error => {
    // 对请求错误做些什么
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    const res = response.data
    
    // 如果是文件下载，直接返回响应对象
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 根据API约定，判断请求是否成功
    // 此处根据后端API的实际响应结构调整
    if (res.success === false || res.error) {
      // 显示错误消息
      ElMessage({
        message: res.error || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      
      return Promise.reject(new Error(res.error || '未知错误'))
    } else {
      return res
    }
  },
  error => {
    // 对响应错误做点什么
    console.error('响应错误:', error)
    
    // 提取错误信息
    let message = error.message || '请求失败'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求错误'
          break
        case 401:
          message = '未授权，请登录'
          // TODO: 处理登录过期逻辑
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = `连接错误 ${error.response.status}`
      }
      
      // 如果响应中包含详细错误信息，优先使用
      if (error.response.data && (error.response.data.error || error.response.data.message)) {
        message = error.response.data.error || error.response.data.message
      }
    }
    
    // 显示错误提示
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    
    return Promise.reject(error)
  }
)

// 导出请求方法
export default service 