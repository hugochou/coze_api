<template>
  <header class="app-header">
    <div class="header-left">
      <el-button type="text" :icon="Expand" class="menu-btn" @click="toggleSidebar" />
      <div class="logo-container">
        <img src="../../assets/logo.svg" alt="Coze API" class="app-logo" />
        <h1 class="app-title">Coze API</h1>
      </div>
    </div>
    <div class="header-right">
      <span class="api-status">
        API服务: 
        <span 
          class="status-indicator" 
          :class="{ 
            'connected': apiStatus.isConnected, 
            'disconnected': !apiStatus.isConnected 
          }"
        ></span>
        {{ apiStatus.isConnected ? '已连接' : '未连接' }}
      </span>
      <el-button type="primary" size="small" @click="checkApiHealth">检查连接</el-button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '../../store/modules/app'
import { Expand } from '@element-plus/icons-vue'

const appStore = useAppStore()

// 计算属性：API状态
const apiStatus = computed(() => appStore.apiStatus)

// 方法：切换侧边栏
const toggleSidebar = () => {
  appStore.toggleSidebar()
}

// 方法：检查API健康状态
const checkApiHealth = async () => {
  try {
    await appStore.checkApiHealth()
  } catch (error) {
    console.error('API服务检查失败:', error)
  }
}
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background-color: #fff;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.logo-container:hover {
  background-color: #f5f7fa;
}

.app-logo {
  height: 32px;
  width: 32px;
  transition: transform 0.3s ease;
}

.logo-container:hover .app-logo {
  transform: rotate(360deg);
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  background: linear-gradient(45deg, #4B79E4, #A44BF1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.menu-btn {
  margin-right: 15px;
}

.api-status {
  margin-right: 15px;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin: 0 5px;
}

.status-indicator.connected {
  background-color: #67c23a;
}

.status-indicator.disconnected {
  background-color: #f56c6c;
}
</style> 