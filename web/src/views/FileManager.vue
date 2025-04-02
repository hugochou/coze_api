<template>
  <div class="file-manager-container">
    <h2 class="page-title">文件管理</h2>
    
    <!-- 文件管理工具栏 -->
    <div class="toolbar">
      <div class="filter-group">
        <el-radio-group 
          v-model="fileType" 
          @change="handleTypeChange"
          size="large"
        >
          <el-radio-button label="all">
            全部 ({{ fileCount.all || 0 }})
          </el-radio-button>
          <el-radio-button label="image">
            图片 ({{ fileCount.image || 0 }})
          </el-radio-button>
          <el-radio-button label="audio">
            音频 ({{ fileCount.audio || 0 }})
          </el-radio-button>
          <el-radio-button label="video">
            视频 ({{ fileCount.video || 0 }})
          </el-radio-button>
        </el-radio-group>
      </div>
      
      <div class="action-group">
        <!-- 全选/取消全选 -->
        <el-checkbox
          v-model="selectAll"
          :indeterminate="isIndeterminate"
          @change="handleSelectAll"
        >
          全选
        </el-checkbox>
        
        <!-- 批量操作按钮 -->
        <el-button
          type="danger"
          :disabled="!hasSelected"
          @click="handleDeleteSelected"
        >
          删除选中 ({{ selectedCount }})
        </el-button>
        
        <!-- 清空按钮 -->
        <el-dropdown @command="handleClear" trigger="click">
          <el-button type="danger">
            清空
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="all">清空所有文件</el-dropdown-item>
              <el-dropdown-item command="image">清空图片文件</el-dropdown-item>
              <el-dropdown-item command="audio">清空音频文件</el-dropdown-item>
              <el-dropdown-item command="video">清空视频文件</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <!-- 刷新按钮 -->
        <el-button @click="refreshFiles">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>
    
    <!-- 文件列表 -->
    <div class="file-list-wrapper" v-loading="loading">
      <template v-if="groupedFiles.length">
        <div 
          v-for="group in groupedFiles" 
          :key="group.date"
          class="file-group"
        >
          <div class="group-header">
            <h3 class="group-title">{{ group.date }}</h3>
          </div>
          
          <div class="files-grid">
            <div 
              v-for="fileItem in group.files" 
              :key="fileItem.path"
              class="file-item"
              :class="{ 'is-selected': isSelected(fileItem) }"
              @click="toggleSelect(fileItem, $event)"
            >
              <!-- 选择框 -->
              <div class="file-select">
                <el-checkbox
                  :model-value="isSelected(fileItem)"
                  @click.stop
                  @change="(val) => handleSelect(fileItem, val)"
                />
              </div>
              
              <!-- 文件预览 -->
              <div 
                class="file-preview"
                @click.stop="openPreview(fileItem)"
              >
                <!-- 图片类型直接显示缩略图 -->
                <img 
                  v-if="fileItem.type === 'image'"
                  :src="formatUrl(fileItem.url)"
                  alt="图片预览"
                />
                
                <!-- 音频类型显示音频图标 -->
                <div 
                  v-else-if="fileItem.type === 'audio'"
                  class="preview-placeholder audio-preview"
                >
                  <el-icon><Microphone /></el-icon>
                </div>
                
                <!-- 视频类型显示视频图标 -->
                <div 
                  v-else-if="fileItem.type === 'video'"
                  class="preview-placeholder video-preview"
                >
                  <el-icon><VideoPlay /></el-icon>
                </div>
                
                <!-- 默认显示文件图标 -->
                <div 
                  v-else
                  class="preview-placeholder file-preview"
                >
                  <el-icon><Document /></el-icon>
                </div>
              </div>
              
              <!-- 文件信息 -->
              <div class="file-info">
                <div class="file-name" :title="fileItem.name">{{ fileItem.name }}</div>
                <div class="file-meta">
                  <span class="file-size">{{ formatSize(fileItem.size) }}</span>
                  <span class="file-time">{{ formatTime(fileItem.modified) }}</span>
                </div>
              </div>
              
              <!-- 文件操作 -->
              <div class="file-actions">
                <el-tooltip content="预览" placement="top">
                  <el-button
                    circle
                    @click.stop="openPreview(fileItem)"
                  >
                    <el-icon><View /></el-icon>
                  </el-button>
                </el-tooltip>
                
                <el-tooltip content="删除" placement="top">
                  <el-button
                    type="danger"
                    circle
                    @click.stop="deleteFile(fileItem)"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 空状态 -->
      <el-empty
        v-else-if="!loading"
        description="没有找到文件"
      >
        <el-button @click="refreshFiles">刷新</el-button>
      </el-empty>
    </div>
    
    <!-- 文件预览对话框 -->
    <el-dialog
      v-if="previewVisible"
      v-model="previewVisible"
      :title="previewFile?.name || '文件预览'"
      width="70%"
      destroy-on-close
    >
      <div class="preview-content">
        <!-- 图片预览 -->
        <div 
          v-if="previewFile && previewFile.type === 'image'"
          class="image-preview"
        >
          <img 
            :src="formatUrl(previewFile.url)" 
            :alt="previewFile.name"
          />
        </div>
        
        <!-- 音频预览 -->
        <div 
          v-else-if="previewFile && previewFile.type === 'audio'"
          class="audio-preview"
        >
          <audio 
            controls
            class="audio-player"
            :src="formatUrl(previewFile.url)"
          >
            您的浏览器不支持音频播放
          </audio>
        </div>
        
        <!-- 视频预览 -->
        <div 
          v-else-if="previewFile && previewFile.type === 'video'"
          class="video-preview"
        >
          <video 
            controls
            class="video-player"
            :src="formatUrl(previewFile.url)"
          >
            您的浏览器不支持视频播放
          </video>
        </div>
        
        <!-- 未知文件类型 -->
        <div v-else class="unknown-preview">
          <el-empty description="无法预览此文件类型" />
        </div>
      </div>
      
      <div class="preview-info" v-if="previewFile">
        <div class="info-item">
          <span class="label">文件名：</span>
          <span class="value">{{ previewFile.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">类型：</span>
          <span class="value">
            {{ previewFile.type === 'image' ? '图片' : 
               previewFile.type === 'audio' ? '音频' : 
               previewFile.type === 'video' ? '视频' : '文件' }}
          </span>
        </div>
        <div class="info-item">
          <span class="label">大小：</span>
          <span class="value">{{ formatSize(previewFile.size) }}</span>
        </div>
        <div class="info-item">
          <span class="label">修改时间：</span>
          <span class="value">{{ previewFile.modified }}</span>
        </div>
        <div class="info-item">
          <span class="label">路径：</span>
          <span class="value">{{ previewFile.path }}</span>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="closePreview">关闭</el-button>
        <el-button 
          type="danger" 
          @click="deletePreviewFile"
        >
          删除
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFileStore } from '../store/modules/file'
import { formatFileSize, getFileUrl } from '../api/file'
import { file } from '../api'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  ArrowDown, 
  Refresh,
  Document,
  Delete,
  View,
  VideoPlay,
  Microphone 
} from '@element-plus/icons-vue'

// 状态管理
const fileStore = useFileStore()

// 本地状态
const fileType = ref('all')
const selectAll = ref(false)
const loading = computed(() => fileStore.loading)

// 计算属性
const fileCount = computed(() => fileStore.fileCount)
const hasSelected = computed(() => fileStore.hasSelected)
const selectedCount = computed(() => fileStore.selectedCount)
const groupedFiles = computed(() => fileStore.groupedFiles)
const isIndeterminate = computed(() => {
  return fileStore.selectedFiles.length > 0 && fileStore.selectedFiles.length < fileStore.files.length
})

// 预览相关
const previewVisible = computed(() => fileStore.previewVisible)
const previewFile = computed(() => fileStore.previewFile)

// 方法
// 切换文件类型筛选
const handleTypeChange = (type) => {
  loadFiles(type)
}

// 加载文件列表
const loadFiles = async (type) => {
  try {
    await fileStore.fetchFiles(type)
    updateSelectAllState()
  } catch (error) {
    console.error('加载文件列表失败:', error)
  }
}

// 刷新文件列表
const refreshFiles = () => {
  loadFiles(fileType.value)
}

// 选择/取消选择文件
const toggleSelect = (fileItem, event) => {
  // 如果点击的是按钮或复选框，不处理
  if (event.target.closest('.file-actions') || event.target.closest('.file-select')) {
    return
  }
  
  fileStore.toggleSelectFile(fileItem)
  updateSelectAllState()
}

// 选择/取消选择文件（通过复选框）
const handleSelect = (fileItem, selected) => {
  if (selected !== fileStore.isSelected(fileItem)) {
    fileStore.toggleSelectFile(fileItem)
  }
  updateSelectAllState()
}

// 全选/取消全选
const handleSelectAll = (val) => {
  fileStore.toggleSelectAll(val)
}

// 更新全选状态
const updateSelectAllState = () => {
  selectAll.value = fileStore.files.length > 0 && 
                   fileStore.selectedFiles.length === fileStore.files.length
}

// 检查文件是否被选中
const isSelected = (fileItem) => {
  return fileStore.isSelected(fileItem)
}

// 删除选中的文件
const handleDeleteSelected = () => {
  fileStore.deleteSelectedFiles()
}

// 清空文件
const handleClear = (type) => {
  fileStore.clearFiles(type)
}

// 预览文件
const openPreview = (fileItem) => {
  fileStore.openPreviewFile(fileItem)
}

// 关闭预览
const closePreview = () => {
  fileStore.closePreview()
}

// 删除当前预览的文件
const deletePreviewFile = async () => {
  try {
    if (!previewFile.value) return
    
    await ElMessageBox.confirm(
      `确定要删除文件 "${previewFile.value.name}" 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 先关闭预览
    fileStore.closePreview()
    
    // 删除文件
    await fileStore.deleteSelectedFiles([previewFile.value])
    
  } catch (error) {
    // 用户取消操作，不做处理
    if (error === 'cancel' || error.toString().includes('cancel')) {
      return
    }
    console.error('删除文件失败:', error)
  }
}

// 删除单个文件
const deleteFile = async (fileItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件 "${fileItem.name}" 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 直接调用API删除文件
    const response = await file.deleteFiles([fileItem.path])
    
    if (response && response.success) {
      // 删除成功后刷新文件列表
      await refreshFiles()
      
      // 显示成功消息
      ElMessage.success(`成功删除文件 ${fileItem.name}`)
    } else {
      throw new Error(response.error || '删除文件失败')
    }
    
  } catch (error) {
    // 用户取消操作，不做处理
    if (error === 'cancel' || error.toString().includes('cancel')) {
      return
    }
    console.error('删除文件失败:', error)
    ElMessage.error(error.message || '删除文件失败')
  }
}

// 格式化文件大小
const formatSize = (size) => {
  return formatFileSize(size)
}

// 格式化时间
const formatTime = (dateTimeStr) => {
  // 只显示时间部分
  const parts = dateTimeStr.split(' ')
  return parts.length > 1 ? parts[1] : dateTimeStr
}

// 获取文件URL
const formatUrl = (url) => {
  return getFileUrl(url)
}

// 组件挂载时加载文件列表
onMounted(() => {
  loadFiles('all')
})

// 监听选中文件变化，更新全选状态
watch(() => fileStore.selectedFiles, () => {
  updateSelectAllState()
}, { deep: true })
</script>

<style scoped>
.file-manager-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.action-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.file-list-wrapper {
  margin-top: 20px;
  min-height: 400px;
}

.file-group {
  margin-bottom: 30px;
}

.group-header {
  margin-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}

.group-title {
  font-size: 18px;
  color: #606266;
  font-weight: 500;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
}

.file-item {
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.file-item:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
}

.file-item.is-selected {
  border: 2px solid #409eff;
}

.file-select {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
}

.file-preview {
  height: 140px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.file-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 40px;
  color: #909399;
}

.audio-preview {
  background-color: #ecf5ff;
}

.video-preview {
  background-color: #f0f9eb;
}

.file-info {
  padding: 10px 15px;
  flex: 1;
}

.file-name {
  margin-bottom: 5px;
  font-size: 14px;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}

.file-actions {
  display: flex;
  justify-content: flex-end;
  padding: 10px 15px;
  gap: 5px;
  border-top: 1px solid #ebeef5;
  background-color: #f8f8f8;
}

/* 预览对话框样式 */
.preview-content {
  text-align: center;
  max-height: 500px;
  overflow: auto;
}

.image-preview img {
  max-width: 100%;
  max-height: 400px;
}

.audio-player, .video-player {
  width: 100%;
}

.preview-info {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 4px;
}

.info-item {
  margin-bottom: 5px;
}

.info-item .label {
  color: #606266;
  font-weight: bold;
  margin-right: 5px;
}
</style> 