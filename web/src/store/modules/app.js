import { defineStore } from 'pinia'
import { getHealthStatus } from '../../api'

export const useAppStore = defineStore('app', {
  state: () => ({
    // API服务状态
    apiStatus: {
      isConnected: false,
      info: null,
      lastCheck: null
    },
    // 侧边栏折叠状态
    sidebarCollapsed: false,
    // 全局加载状态
    loading: false
  }),
  
  getters: {
    // 判断API是否可用
    isApiAvailable: (state) => state.apiStatus.isConnected
  },
  
  actions: {
    // 检查API服务健康状态
    async checkApiHealth() {
      try {
        this.loading = true
        const response = await getHealthStatus()
        
        // 更新API状态
        this.apiStatus = {
          isConnected: true,
          info: response,
          lastCheck: new Date()
        }
        
        return response
      } catch (error) {
        console.error('API健康检查失败:', error)
        
        // 更新API状态为不可用
        this.apiStatus = {
          isConnected: false,
          info: null,
          lastCheck: new Date()
        }
        
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 切换侧边栏折叠状态
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    // 设置全局加载状态
    setLoading(status) {
      this.loading = status
    }
  }
}) 