<template>
  <div class="videos-container">
    <h2 class="page-title">视频管理</h2>
    
    <div class="top-actions">
      <el-button 
        type="primary" 
        icon="Plus" 
        @click="$router.push('/creator')"
      >
        创建新视频
      </el-button>
      
      <el-button 
        icon="Refresh" 
        plain 
        @click="refreshVideos"
        :loading="loading"
      >
        刷新列表
      </el-button>
    </div>
    
    <!-- 视频列表 -->
    <div class="panel" v-loading="loading">
      <el-empty 
        description="暂无视频，点击'创建新视频'开始" 
        v-if="!videos.length && !loading"
      />
      
      <div class="videos-list" v-else>
        <el-card 
          v-for="video in videos" 
          :key="video.filename"
          class="video-card"
          :class="{ 'active': selectedVideo && selectedVideo.filename === video.filename }"
          @click="selectVideo(video)"
        >
          <div class="video-info">
            <div class="video-thumbnail">
              <el-icon class="video-icon"><VideoPlay /></el-icon>
            </div>
            <div class="video-details">
              <h3 class="video-name">{{ formatVideoName(video.filename) }}</h3>
              <p class="video-meta">
                <span>大小: {{ formatFileSize(video.size) }}</span>
                <span>创建时间: {{ formatDate(video.created_at) }}</span>
              </p>
            </div>
            <div class="video-actions">
              <el-button 
                type="primary" 
                size="small" 
                icon="VideoPlay"
                @click.stop="playVideo(video)"
              >
                播放
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                icon="Download"
                @click.stop="downloadVideo(video)"
              >
                下载
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 视频播放面板 -->
    <div class="panel" v-if="selectedVideo">
      <div class="panel-header">
        <h3 class="panel-title">视频预览</h3>
        <el-button 
          type="text" 
          icon="Close" 
          @click="selectedVideo = null"
        >
          关闭预览
        </el-button>
      </div>
      
      <div class="video-player">
        <video controls :src="getVideoUrl(selectedVideo)" class="video-element"></video>
      </div>
      
      <div class="video-details-full">
        <h4>视频信息</h4>
        <p><strong>文件名:</strong> {{ selectedVideo.filename }}</p>
        <p><strong>文件大小:</strong> {{ formatFileSize(selectedVideo.size) }}</p>
        <p><strong>创建时间:</strong> {{ formatDate(selectedVideo.created_at) }}</p>
        <p><strong>视频链接:</strong> <el-link :href="getVideoUrl(selectedVideo)" target="_blank">{{ getVideoUrl(selectedVideo) }}</el-link></p>
        
        <div class="video-actions-full">
          <el-button 
            type="success" 
            icon="Download"
            @click="downloadVideo(selectedVideo)"
          >
            下载视频
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      :closable="false"
      show-icon
      style="margin-top: 20px"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { VideoPlay, Download, Plus, Refresh, Close } from '@element-plus/icons-vue'
import { useVideoStore } from '../store/modules/video'
import { video } from '../api'

const router = useRouter()
const videoStore = useVideoStore()

// 状态
const selectedVideo = ref(null)
const loading = computed(() => videoStore.loading)
const videos = computed(() => videoStore.videos)
const error = computed(() => videoStore.error)

// 获取视频URL
const getVideoUrl = (videoItem) => {
  if (!videoItem) return ''
  return videoItem.full_url || video.getVideoUrl(videoItem.filename)
}

// 格式化视频名称
const formatVideoName = (filename) => {
  if (!filename) return '未命名视频'
  
  // 去除前缀和后缀
  let name = filename.replace(/^video_/, '')
  name = name.replace(/\.\w+$/, '')
  
  // 格式化日期部分
  name = name.replace(/(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})/, '$1-$2-$3 $4:$5:$6')
  
  return name
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '未知'
  
  if (size < 1024) {
    return size + ' B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  } else {
    return (size / (1024 * 1024)).toFixed(2) + ' MB'
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  
  // 如果已经是格式化的日期，直接返回
  if (dateStr.includes('-') && dateStr.includes(':')) {
    return dateStr
  }
  
  // 尝试解析日期字符串
  try {
    const date = new Date(dateStr)
    return date.toLocaleString()
  } catch (e) {
    return dateStr
  }
}

// 选择视频
const selectVideo = (videoItem) => {
  selectedVideo.value = videoItem
}

// 播放视频
const playVideo = (videoItem) => {
  selectedVideo.value = videoItem
  
  // 滚动到播放器位置
  setTimeout(() => {
    document.querySelector('.video-player')?.scrollIntoView({ behavior: 'smooth' })
  }, 100)
}

// 下载视频
const downloadVideo = (videoItem) => {
  if (!videoItem || !videoItem.filename) {
    ElMessage.warning('无效的视频文件')
    return
  }
  
  video.downloadVideo(videoItem.filename)
  ElMessage.success('开始下载视频')
}

// 刷新视频列表
const refreshVideos = async () => {
  try {
    await videoStore.fetchVideos()
    ElMessage.success('视频列表已更新')
  } catch (error) {
    console.error('刷新视频列表失败:', error)
    // 错误处理由Store完成
  }
}

// 组件挂载时获取视频列表
onMounted(async () => {
  videoStore.clearError()
  await refreshVideos()
})
</script>

<style scoped>
.videos-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.top-actions {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-bottom: 20px;
}

.panel {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.panel-title {
  font-size: 18px;
  margin-bottom: 0;
  color: #303133;
}

.videos-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.video-card {
  cursor: pointer;
  transition: all 0.3s;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-card.active {
  border-color: #409eff;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.2);
}

.video-info {
  display: flex;
  align-items: center;
}

.video-thumbnail {
  width: 80px;
  height: 60px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.video-icon {
  font-size: 24px;
  color: #409eff;
}

.video-details {
  flex: 1;
}

.video-name {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 5px;
  color: #303133;
}

.video-meta {
  font-size: 12px;
  color: #909399;
  margin: 0;
  display: flex;
  gap: 15px;
}

.video-actions {
  display: flex;
  gap: 10px;
}

.video-player {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

.video-element {
  width: 100%;
  max-width: 800px;
  max-height: 450px;
  background-color: #000;
}

.video-details-full {
  margin-top: 20px;
}

.video-details-full h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #303133;
}

.video-details-full p {
  margin: 5px 0;
  color: #606266;
}

.video-actions-full {
  margin-top: 15px;
}
</style> 