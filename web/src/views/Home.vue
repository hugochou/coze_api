<template>
  <div class="home-container">
    <div class="welcome-panel panel">
      <h2 class="welcome-title">欢迎使用 Coze API 管理平台</h2>
      <p class="welcome-desc">这是一个用于测试和管理Coze API功能的Web界面，您可以通过该平台轻松地使用所有API功能。</p>
      
      <el-divider />
      
      <div class="api-status-panel">
        <h3>API服务状态</h3>
        <div class="status-info" v-if="apiStatus.isConnected">
          <el-alert
            title="API服务正常运行中"
            type="success"
            :closable="false"
            show-icon
          >
            <template #default>
              <p>服务器环境: {{ apiStatus.info?.environment || '未知' }}</p>
              <p>上次检查时间: {{ lastCheckTime }}</p>
            </template>
          </el-alert>
        </div>
        <div class="status-info" v-else>
          <el-alert
            title="API服务连接失败"
            type="error"
            :closable="false"
            show-icon
          >
            <template #default>
              <p>请检查API服务是否正常运行，或者网络连接是否正常。</p>
              <el-button type="primary" size="small" @click="checkApiHealth">重新检查</el-button>
            </template>
          </el-alert>
        </div>
      </div>
    </div>
    
    <div class="features-panel panel">
      <h3 class="panel-title">功能导航</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/upload')">
            <template #header>
              <div class="feature-header">
                <el-icon><Upload /></el-icon>
                <span>上传管理</span>
              </div>
            </template>
            <div class="feature-content">
              上传和管理图片与音频文件，支持预览和删除操作。
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/creator')">
            <template #header>
              <div class="feature-header">
                <el-icon><VideoCamera /></el-icon>
                <span>视频创建</span>
              </div>
            </template>
            <div class="feature-content">
              创建视频，设置动画效果、转场效果和音频，支持预览。
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/videos')">
            <template #header>
              <div class="feature-header">
                <el-icon><VideoPlay /></el-icon>
                <span>视频管理</span>
              </div>
            </template>
            <div class="feature-content">
              管理已创建的视频，支持播放、下载和删除操作。
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '../store/modules/app'
import { Upload, VideoCamera, VideoPlay } from '@element-plus/icons-vue'

const appStore = useAppStore()

// API状态
const apiStatus = computed(() => appStore.apiStatus)

// 格式化上次检查时间
const lastCheckTime = computed(() => {
  if (!apiStatus.value.lastCheck) return '未检查'
  return new Date(apiStatus.value.lastCheck).toLocaleString()
})

// 重新检查API状态
const checkApiHealth = async () => {
  try {
    await appStore.checkApiHealth()
  } catch (error) {
    console.error('API健康检查失败:', error)
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-panel {
  margin-bottom: 30px;
}

.welcome-title {
  font-size: 24px;
  margin-bottom: 10px;
  color: #303133;
}

.welcome-desc {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
}

.api-status-panel {
  margin-top: 20px;
}

.status-info {
  margin-top: 15px;
}

.features-panel {
  margin-bottom: 30px;
}

.feature-header {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.feature-header .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.feature-content {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.el-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style> 