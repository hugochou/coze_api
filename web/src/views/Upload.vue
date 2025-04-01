<template>
  <div class="upload-container">
    <h2 class="page-title">上传管理</h2>
    
    <el-tabs v-model="activeTab" class="upload-tabs">
      <el-tab-pane label="图片上传" name="image">
        <div class="upload-panel panel">
          <div class="upload-area">
            <el-upload
              class="upload-dropzone"
              drag
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleImageChange"
              accept="image/*"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                将图片拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持JPG/PNG/JPEG/GIF格式图片
                </div>
              </template>
            </el-upload>
            
            <div class="upload-actions" v-if="selectedImage">
              <p class="selected-file">已选择: {{ selectedImage.name }}</p>
              <el-button type="primary" @click="uploadImage" :loading="uploading">
                上传图片
              </el-button>
            </div>
          </div>
          
          <el-divider>已上传图片列表</el-divider>
          
          <div class="uploaded-list" v-loading="loading">
            <el-empty description="暂无已上传图片" v-if="!uploadedImages.length" />
            
            <el-row :gutter="20" v-else>
              <el-col :span="6" v-for="(item, index) in uploadedImages" :key="index">
                <el-card shadow="hover" class="image-card">
                  <img :src="getImageUrl(item)" class="image-preview" />
                  <div class="image-info">
                    <p class="image-name">{{ item.originalName || '未命名图片' }}</p>
                    <div class="image-actions">
                      <el-button type="primary" size="small" @click="previewImage(item)">
                        预览
                      </el-button>
                      <el-button type="danger" size="small" @click="removeImage(item)">
                        删除
                      </el-button>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="音频上传" name="audio">
        <div class="upload-panel panel">
          <div class="upload-area">
            <el-upload
              class="upload-dropzone"
              drag
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleAudioChange"
              accept="audio/*"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                将音频拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持MP3/WAV/OGG/M4A格式音频
                </div>
              </template>
            </el-upload>
            
            <div class="upload-actions" v-if="selectedAudio">
              <p class="selected-file">已选择: {{ selectedAudio.name }}</p>
              <el-button type="primary" @click="uploadAudio" :loading="uploading">
                上传音频
              </el-button>
            </div>
          </div>
          
          <el-divider>已上传音频列表</el-divider>
          
          <div class="uploaded-list" v-loading="loading">
            <el-empty description="暂无已上传音频" v-if="!uploadedAudios.length" />
            
            <el-table :data="uploadedAudios" v-else style="width: 100%">
              <el-table-column prop="originalName" label="文件名" width="250" />
              <el-table-column label="预览">
                <template #default="{ row }">
                  <audio controls style="width: 300px">
                    <source :src="getAudioUrl(row)" />
                    您的浏览器不支持音频标签
                  </audio>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150">
                <template #default="{ row }">
                  <el-button type="danger" size="small" @click="removeAudio(row)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 图片预览对话框 -->
    <el-dialog 
      v-model="imagePreview.visible" 
      :title="imagePreview.title" 
      width="50%"
      center
    >
      <div class="preview-container">
        <img :src="imagePreview.url" class="preview-image" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUploadStore } from '../store/modules/upload'
import { upload } from '../api'

// 状态管理
const uploadStore = useUploadStore()

// 本地状态
const activeTab = ref('image')
const selectedImage = ref(null)
const selectedAudio = ref(null)
const loading = ref(false)
const uploading = ref(false)
const imagePreview = ref({
  visible: false,
  url: '',
  title: ''
})

// 获取上传列表
const uploadedImages = computed(() => uploadStore.uploadedImages || [])
const uploadedAudios = computed(() => uploadStore.uploadedAudios || [])

// 获取图片URL
const getImageUrl = (item) => {
  return item.full_url || upload.getFileUrl(item.url)
}

// 获取音频URL
const getAudioUrl = (item) => {
  return item.full_url || upload.getFileUrl(item.url)
}

// 处理图片选择
const handleImageChange = (file) => {
  selectedImage.value = file.raw
}

// 处理音频选择
const handleAudioChange = (file) => {
  selectedAudio.value = file.raw
}

// 上传图片
const uploadImage = async () => {
  if (!selectedImage.value) {
    ElMessage.warning('请先选择一张图片')
    return
  }
  
  try {
    uploading.value = true
    await uploadStore.uploadImage(selectedImage.value)
    ElMessage.success('图片上传成功')
    selectedImage.value = null
  } catch (error) {
    console.error('上传图片失败:', error)
    ElMessage.error('上传图片失败: ' + (error.message || '未知错误'))
  } finally {
    uploading.value = false
  }
}

// 上传音频
const uploadAudio = async () => {
  if (!selectedAudio.value) {
    ElMessage.warning('请先选择一个音频文件')
    return
  }
  
  try {
    uploading.value = true
    await uploadStore.uploadAudio(selectedAudio.value)
    ElMessage.success('音频上传成功')
    selectedAudio.value = null
  } catch (error) {
    console.error('上传音频失败:', error)
    ElMessage.error('上传音频失败: ' + (error.message || '未知错误'))
  } finally {
    uploading.value = false
  }
}

// 预览图片
const previewImage = (item) => {
  imagePreview.value = {
    visible: true,
    url: getImageUrl(item),
    title: item.originalName || '图片预览'
  }
}

// 删除图片
const removeImage = (item) => {
  uploadStore.removeUploadedImage(item.id)
  ElMessage.success('图片已删除')
}

// 删除音频
const removeAudio = (item) => {
  uploadStore.removeUploadedAudio(item.id)
  ElMessage.success('音频已删除')
}

// 组件挂载时加载数据
onMounted(() => {
  // TODO: 如果需要，在此处加载上传历史
})
</script>

<style scoped>
.upload-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.upload-tabs {
  margin-top: 20px;
}

.upload-panel {
  margin-top: 20px;
}

.upload-area {
  max-width: 500px;
  margin: 0 auto 30px;
}

.upload-actions {
  margin-top: 15px;
  text-align: center;
}

.selected-file {
  margin-bottom: 10px;
  color: #606266;
}

.uploaded-list {
  margin-top: 20px;
}

.image-card {
  margin-bottom: 20px;
  height: 100%;
}

.image-preview {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-info {
  margin-top: 10px;
}

.image-name {
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-actions {
  display: flex;
  justify-content: space-between;
}

.preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-image {
  max-width: 100%;
  max-height: 500px;
}
</style> 