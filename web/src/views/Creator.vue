<template>
  <div class="creator-container">
    <h2 class="page-title">视频创建</h2>
    
    <!-- 页面布局，左侧上传图片列表，右侧时间线和配置 -->
    <el-row :gutter="20">
      <!-- 左侧面板：已上传图片 -->
      <el-col :span="8">
        <div class="panel">
          <h3 class="panel-title">选择图片</h3>
          <div v-loading="uploading">
            <el-empty description="暂无已上传图片" v-if="!uploadedImages.length">
              <el-button type="primary" @click="$router.push('/upload')">
                上传图片
              </el-button>
            </el-empty>
            
            <div class="image-list" v-else>
              <div 
                v-for="image in uploadedImages" 
                :key="image.id"
                class="image-item"
                :class="{ selected: isImageSelected(image.id) }"
                @click="selectImage(image)"
              >
                <img :src="getImageUrl(image)" class="image-thumbnail" />
                <div class="image-caption">{{ image.originalName || '未命名图片' }}</div>
                <div class="image-actions">
                  <el-button 
                    type="primary" 
                    size="small" 
                    icon="Plus"
                    @click.stop="addImageToVideo(image)"
                    :disabled="isImageInVideo(image.id)"
                  >
                    添加到视频
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="panel">
          <h3 class="panel-title">视频参数配置</h3>
          
          <el-form :model="videoConfig" label-position="top">
            <el-form-item label="转场效果">
              <el-select v-model="videoConfig.transition" class="w-full">
                <el-option label="淡入淡出" value="淡入淡出" />
                <el-option label="滑动" value="滑动" />
                <el-option label="缩放" value="缩放" />
                <el-option label="旋转" value="旋转" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="转场时长(秒)">
              <el-slider 
                v-model="videoConfig.transition_duration" 
                :min="0.2" 
                :max="2" 
                :step="0.1" 
                show-input 
              />
            </el-form-item>
            
            <el-form-item label="输出帧率">
              <el-radio-group v-model="videoConfig.output_fps">
                <el-radio :label="24">24 fps</el-radio>
                <el-radio :label="30">30 fps</el-radio>
                <el-radio :label="60">60 fps</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="输出质量">
              <el-radio-group v-model="videoConfig.output_quality">
                <el-radio label="low">低</el-radio>
                <el-radio label="medium">中</el-radio>
                <el-radio label="high">高</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      
      <!-- 右侧面板：视频时间线和当前图片配置 -->
      <el-col :span="16">
        <div class="panel">
          <div class="panel-header">
            <h3 class="panel-title">视频时间线</h3>
            <div class="panel-actions">
              <el-button 
                type="danger" 
                plain 
                icon="Delete" 
                size="small"
                @click="clearTimeline"
                :disabled="!videoImages.length"
              >
                清空
              </el-button>
            </div>
          </div>
          
          <el-empty 
            description="请从左侧添加图片到时间线" 
            v-if="!videoImages.length"
          />
          
          <div class="timeline" v-else>
            <el-card 
              v-for="(image, index) in sortedVideoImages" 
              :key="image.id"
              class="timeline-item"
              :class="{ active: selectedImageId === image.id }"
              @click="selectedImageId = image.id"
            >
              <div class="timeline-item-header">
                <span class="timeline-item-index">{{ index + 1 }}</span>
                <img :src="getImageUrl(findOriginalImage(image.id))" class="timeline-item-thumb" />
                <el-dropdown trigger="click" @command="handleTimelineAction">
                  <el-button type="text" icon="More" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item 
                        :command="{ action: 'move-up', id: image.id }"
                        :disabled="index === 0"
                      >
                        上移
                      </el-dropdown-item>
                      <el-dropdown-item 
                        :command="{ action: 'move-down', id: image.id }"
                        :disabled="index === videoImages.length - 1"
                      >
                        下移
                      </el-dropdown-item>
                      <el-dropdown-item :command="{ action: 'remove', id: image.id }">
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              
              <div class="timeline-item-body">
                <div class="timeline-item-settings">
                  <el-form label-position="left" label-width="80px" size="small">
                    <el-form-item label="持续时间">
                      <el-input-number 
                        v-model="image.duration" 
                        :min="1" 
                        :max="10" 
                        :step="0.5"
                        @change="updateDuration(image.id, $event)"
                      />
                      秒
                    </el-form-item>
                    
                    <el-form-item label="图片文本">
                      <el-input 
                        type="textarea" 
                        v-model="image.text" 
                        :rows="2"
                        placeholder="添加描述文本，可用于生成配音"
                        @change="updateImageText(image.id, $event)"
                      />
                      <div class="text-actions" v-if="image.text">
                        <el-button 
                          type="primary" 
                          size="small" 
                          @click="generateAudioFromText(image.id)"
                          :loading="generatingAudio === image.id"
                        >
                          生成配音
                        </el-button>
                      </div>
                    </el-form-item>
                    
                    <el-form-item label="动画效果">
                      <el-select 
                        v-model="image.animation.name"
                        @change="(val) => updateAnimation(image.id, 'name', val)"
                      >
                        <el-option label="缩放" value="缩放" />
                        <el-option label="平移" value="平移" />
                        <el-option label="缩放平移" value="缩放平移" />
                        <el-option label="旋转" value="旋转" />
                        <el-option label="淡入淡出" value="淡入淡出" />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="音频">
                      <el-select 
                        v-model="selectedAudioId[image.id]" 
                        placeholder="选择音频"
                        clearable
                        @change="(val) => setImageAudio(image.id, val)"
                      >
                        <el-option 
                          v-for="audio in uploadedAudios" 
                          :key="audio.id"
                          :label="audio.originalName || '未命名音频'"
                          :value="audio.path"
                        />
                      </el-select>
                    </el-form-item>
                  </el-form>
                </div>
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 动画配置详情面板 -->
        <div class="panel" v-if="selectedImage">
          <div class="panel-header">
            <h3 class="panel-title">动画详细配置</h3>
            <div class="panel-actions">
              <el-button-group>
                <el-tooltip content="查看动画效果预览" placement="top">
                  <el-button 
                    type="primary" 
                    plain 
                    icon="View" 
                    @click="previewAnimation"
                    :disabled="!isAnimationPreviewAvailable"
                  >
                    预览
                  </el-button>
                </el-tooltip>
                <el-dropdown trigger="click" @command="applyAnimationPreset">
                  <el-button type="primary" plain>
                    应用预设
                    <el-icon class="el-icon--right"><arrow-down /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="zoomIn">缓慢放大</el-dropdown-item>
                      <el-dropdown-item command="zoomOut">缓慢缩小</el-dropdown-item>
                      <el-dropdown-item command="panRight">向右平移</el-dropdown-item>
                      <el-dropdown-item command="panLeft">向左平移</el-dropdown-item>
                      <el-dropdown-item command="kenBurns">肯Burns效果</el-dropdown-item>
                      <el-dropdown-item command="dramaticZoom">戏剧性放大</el-dropdown-item>
                      <el-dropdown-item command="gentleSway">轻微摇摆</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-button-group>
            </div>
          </div>
          
          <div class="animation-settings">
            <el-form-item label="动画曲线" v-if="selectedImage.animation.name !== '淡入淡出'">
              <el-select 
                v-model="selectedImage.animation.easing" 
                placeholder="选择动画曲线"
                @change="(val) => updateAnimation(selectedImage.id, 'easing', val)"
              >
                <el-option label="线性" value="linear" />
                <el-option label="缓入" value="easeIn" />
                <el-option label="缓出" value="easeOut" />
                <el-option label="缓入缓出" value="easeInOut" />
              </el-select>
            </el-form-item>
            
            <div v-if="['缩放', '缩放平移'].includes(selectedImage.animation.name)">
              <h4>缩放设置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="初始缩放">
                    <el-slider 
                      v-model="selectedImage.animation.scale_from" 
                      :min="0.5" 
                      :max="2" 
                      :step="0.1" 
                      @change="(val) => updateAnimation(selectedImage.id, 'scale_from', val)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="结束缩放">
                    <el-slider 
                      v-model="selectedImage.animation.scale_to" 
                      :min="0.5" 
                      :max="2" 
                      :step="0.1" 
                      @change="(val) => updateAnimation(selectedImage.id, 'scale_to', val)"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
            
            <div v-if="['平移', '缩放平移'].includes(selectedImage.animation.name)">
              <h4>位置设置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <p>初始位置</p>
                  <el-row>
                    <el-col :span="12">
                      <el-form-item label="X">
                        <el-slider 
                          v-model="selectedImage.animation.position_from[0]" 
                          :min="0" 
                          :max="1" 
                          :step="0.1" 
                          @change="updatePositionFrom"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Y">
                        <el-slider 
                          v-model="selectedImage.animation.position_from[1]" 
                          :min="0" 
                          :max="1" 
                          :step="0.1" 
                          @change="updatePositionFrom"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-col>
                <el-col :span="12">
                  <p>结束位置</p>
                  <el-row>
                    <el-col :span="12">
                      <el-form-item label="X">
                        <el-slider 
                          v-model="selectedImage.animation.position_to[0]" 
                          :min="0" 
                          :max="1" 
                          :step="0.1" 
                          @change="updatePositionTo"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Y">
                        <el-slider 
                          v-model="selectedImage.animation.position_to[1]" 
                          :min="0" 
                          :max="1" 
                          :step="0.1" 
                          @change="updatePositionTo"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-col>
              </el-row>
            </div>
            
            <div v-if="selectedImage.animation.name === '旋转'">
              <h4>旋转设置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="初始角度">
                    <el-slider 
                      v-model="selectedImage.animation.rotate_from" 
                      :min="-180" 
                      :max="180" 
                      @change="(val) => updateAnimation(selectedImage.id, 'rotate_from', val)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="结束角度">
                    <el-slider 
                      v-model="selectedImage.animation.rotate_to" 
                      :min="-180" 
                      :max="180" 
                      @change="(val) => updateAnimation(selectedImage.id, 'rotate_to', val)"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
            
            <div v-if="selectedImage.animation.name === '淡入淡出'">
              <h4>透明度设置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="初始透明度">
                    <el-slider 
                      v-model="selectedImage.animation.opacity_from" 
                      :min="0" 
                      :max="1" 
                      :step="0.1" 
                      @change="(val) => updateAnimation(selectedImage.id, 'opacity_from', val)"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="结束透明度">
                    <el-slider 
                      v-model="selectedImage.animation.opacity_to" 
                      :min="0" 
                      :max="1" 
                      :step="0.1" 
                      @change="(val) => updateAnimation(selectedImage.id, 'opacity_to', val)"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
            
            <div class="animation-preview" v-if="isShowingPreview">
              <h4>动画效果预览</h4>
              <div class="preview-container" ref="previewContainer">
                <img 
                  :src="getPreviewImageUrl()" 
                  ref="previewImage" 
                  class="preview-target"
                  :style="previewImageStyle"
                />
              </div>
              
              <div class="preview-controls">
                <el-slider 
                  v-model="previewProgress" 
                  :min="0" 
                  :max="100" 
                  @input="updatePreview"
                />
                <div class="preview-buttons">
                  <el-button size="small" @click="playPreview">播放</el-button>
                  <el-button size="small" @click="resetPreview">重置</el-button>
                  <el-button size="small" @click="isShowingPreview = false">关闭</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="create-actions">
          <el-alert 
            v-if="error" 
            :title="error" 
            type="error" 
            :closable="false" 
            show-icon 
            style="margin-bottom: 15px"
          />
          
          <el-button 
            type="primary" 
            icon="VideoPlay" 
            :disabled="!canCreateVideo" 
            :loading="creating"
            @click="createVideo"
          >
            生成视频
          </el-button>
          
          <p class="help-text" v-if="!canCreateVideo">
            请至少添加一张图片到时间线
          </p>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, More, VideoPlay, ArrowDown, View } from '@element-plus/icons-vue'
import { useUploadStore } from '../store/modules/upload'
import { useVideoStore } from '../store/modules/video'
import { useAudioStore } from '../store/modules/audio'
import { upload, audio } from '../api'

const router = useRouter()
const uploadStore = useUploadStore()
const videoStore = useVideoStore()
const audioStore = useAudioStore()

// 上传状态
const uploading = ref(false)

// 本地状态
const selectedImageId = ref(null)
const selectedAudioId = reactive({}) // 存储每个图片关联的音频ID

// 文本转音频状态
const generatingAudio = ref(null) // 正在生成音频的图片ID

// 动画预览状态
const isShowingPreview = ref(false)
const previewProgress = ref(0)
const previewContainer = ref(null)
const previewImage = ref(null)
const previewImageStyle = ref({
  transform: 'scale(1) translate(0%, 0%)',
  opacity: '1',
  transformOrigin: 'center',
  transition: 'none'
})

// 动画预览计时器
let previewTimer = null

// 获取上传列表
const uploadedImages = computed(() => uploadStore.uploadedImages || [])
const uploadedAudios = computed(() => uploadStore.uploadedAudios || [])

// 获取视频创建状态
const videoImages = computed(() => videoStore.videoImages)
const sortedVideoImages = computed(() => {
  return [...videoImages.value].sort((a, b) => a.order - b.order)
})
const videoConfig = computed(() => videoStore.videoConfig)
const creating = computed(() => videoStore.creating)
const error = computed(() => videoStore.error)
const canCreateVideo = computed(() => videoStore.canCreateVideo)

// 获取选中的图片
const selectedImage = computed(() => {
  if (!selectedImageId.value) return null
  return videoImages.value.find(img => img.id === selectedImageId.value)
})

// 获取图片URL
const getImageUrl = (item) => {
  if (!item) return ''
  return item.full_url || upload.getFileUrl(item.url)
}

// 检查图片是否被选中
const isImageSelected = (id) => {
  return selectedImageId.value === id
}

// 检查图片是否已在视频中
const isImageInVideo = (id) => {
  return videoImages.value.some(img => img.id === id)
}

// 查找原始图片
const findOriginalImage = (id) => {
  return uploadedImages.value.find(img => img.id === id) || {}
}

// 选择图片
const selectImage = (image) => {
  selectedImageId.value = image.id
}

// 添加图片到视频
const addImageToVideo = (image) => {
  if (isImageInVideo(image.id)) return
  
  const newItem = videoStore.addImageToVideo(image)
  selectedImageId.value = newItem.id
  
  ElMessage.success('图片已添加到时间线')
}

// 清空时间线
const clearTimeline = () => {
  ElMessageBox.confirm('确定要清空时间线吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    videoStore.resetVideoCreation()
    selectedImageId.value = null
    ElMessage.success('时间线已清空')
  }).catch(() => {})
}

// 处理时间线操作
const handleTimelineAction = ({ action, id }) => {
  if (action === 'remove') {
    videoStore.removeImageFromVideo(id)
    if (selectedImageId.value === id) {
      selectedImageId.value = null
    }
    ElMessage.success('已从时间线移除')
  } else if (action === 'move-up' || action === 'move-down') {
    const images = [...sortedVideoImages.value]
    const index = images.findIndex(img => img.id === id)
    
    if (index === -1) return
    
    const newIndex = action === 'move-up' ? index - 1 : index + 1
    if (newIndex < 0 || newIndex >= images.length) return
    
    // 交换位置
    const temp = images[index]
    images[index] = images[newIndex]
    images[newIndex] = temp
    
    // 更新顺序
    const newOrder = images.map(img => img.id)
    videoStore.reorderVideoImages(newOrder)
  }
}

// 更新持续时间
const updateDuration = (id, value) => {
  videoStore.updateVideoImage(id, { duration: value })
}

// 更新动画属性
const updateAnimation = (id, key, value) => {
  const image = videoImages.value.find(img => img.id === id)
  if (!image) return
  
  const animation = { ...image.animation }
  animation[key] = value
  
  videoStore.updateVideoImage(id, { animation })
}

// 更新初始位置
const updatePositionFrom = () => {
  if (!selectedImage.value) return
  
  const position = [...selectedImage.value.animation.position_from]
  updateAnimation(selectedImage.value.id, 'position_from', position)
}

// 更新结束位置
const updatePositionTo = () => {
  if (!selectedImage.value) return
  
  const position = [...selectedImage.value.animation.position_to]
  updateAnimation(selectedImage.value.id, 'position_to', position)
}

// 设置图片音频
const setImageAudio = (imageId, audioPath) => {
  videoStore.setImageAudio(imageId, audioPath)
}

// 创建视频
const createVideo = async () => {
  try {
    const result = await videoStore.createVideo()
    
    if (result) {
      ElMessage.success('视频创建成功')
      router.push('/videos')
    }
  } catch (error) {
    console.error('创建视频失败:', error)
    // 错误处理由Store完成
  }
}

// 检查是否可以预览动画
const isAnimationPreviewAvailable = computed(() => {
  if (!selectedImage.value) return false
  
  // 确保有动画属性
  const animation = selectedImage.value.animation
  if (!animation || !animation.name) return false
  
  return true
})

// 获取预览图片的URL
const getPreviewImageUrl = () => {
  if (!selectedImage.value) return ''
  
  const originalImage = findOriginalImage(selectedImage.value.id)
  return getImageUrl(originalImage)
}

// 更新图片文本
const updateImageText = (id, text) => {
  videoStore.updateVideoImage(id, { text })
}

// 从文本生成音频
const generateAudioFromText = async (imageId) => {
  const imageItem = videoImages.value.find(img => img.id === imageId)
  if (!imageItem || !imageItem.text) {
    ElMessage.warning('请先添加图片文本')
    return
  }
  
  try {
    generatingAudio.value = imageId
    
    // 调用文本转音频API
    const result = await audioStore.createAudio({
      text: imageItem.text,
      voice: 'zh-CN',
      speed: 1.0,
      format: 'mp3'
    })
    
    // 设置生成的音频为图片的配音
    if (result && result.path) {
      videoStore.setImageAudio(imageId, result.path)
      selectedAudioId[imageId] = result.path
      
      // 添加到已上传音频列表，方便后续使用
      if (!uploadStore.uploadedAudios.some(a => a.path === result.path)) {
        uploadStore.addGeneratedAudio({
          id: Date.now().toString(),
          originalName: `${imageItem.text.substring(0, 10)}... 生成的音频`,
          path: result.path,
          url: result.url,
          full_url: result.full_url
        })
      }
      
      ElMessage.success('音频生成成功')
    }
  } catch (error) {
    console.error('生成音频失败:', error)
    ElMessage.error('生成音频失败: ' + (error.message || '未知错误'))
  } finally {
    generatingAudio.value = null
  }
}

// 应用动画预设
const applyAnimationPreset = (preset) => {
  if (!selectedImage.value) return
  
  const animation = { ...selectedImage.value.animation }
  const id = selectedImage.value.id
  
  switch (preset) {
    case 'zoomIn':
      animation.name = '缩放'
      animation.scale_from = 1.0
      animation.scale_to = 1.3
      animation.easing = 'easeInOut'
      break
      
    case 'zoomOut':
      animation.name = '缩放'
      animation.scale_from = 1.3
      animation.scale_to = 1.0
      animation.easing = 'easeInOut'
      break
      
    case 'panRight':
      animation.name = '平移'
      animation.position_from = [0.4, 0.5]
      animation.position_to = [0.6, 0.5]
      animation.easing = 'linear'
      break
      
    case 'panLeft':
      animation.name = '平移'
      animation.position_from = [0.6, 0.5]
      animation.position_to = [0.4, 0.5]
      animation.easing = 'linear'
      break
      
    case 'kenBurns':
      animation.name = '缩放平移'
      animation.scale_from = 1.0
      animation.scale_to = 1.2
      animation.position_from = [0.5, 0.5]
      animation.position_to = [0.6, 0.4]
      animation.easing = 'easeInOut'
      break
      
    case 'dramaticZoom':
      animation.name = '缩放'
      animation.scale_from = 1.0
      animation.scale_to = 1.5
      animation.easing = 'easeIn'
      break
      
    case 'gentleSway':
      animation.name = '平移'
      animation.position_from = [0.48, 0.5]
      animation.position_to = [0.52, 0.5]
      animation.easing = 'easeInOut'
      break
  }
  
  videoStore.updateVideoImage(id, { animation })
  ElMessage.success('已应用动画预设')
}

// 预览动画效果
const previewAnimation = async () => {
  if (!selectedImage.value) return
  
  isShowingPreview.value = true
  previewProgress.value = 0
  
  // 等待DOM更新完成
  await nextTick()
  
  // 初始化预览
  updatePreview(0)
}

// 更新预览效果
const updatePreview = (progress) => {
  if (!selectedImage.value) return
  
  const animation = selectedImage.value.animation
  const style = {}
  
  // 比例计算 (0-100% => 0-1)
  const t = progress / 100
  
  // 根据动画类型应用不同的变换
  if (animation.name === '缩放' || animation.name === '缩放平移') {
    // 缩放计算
    const scale = animation.scale_from + (animation.scale_to - animation.scale_from) * t
    style.transform = `scale(${scale})`
  }
  
  if (animation.name === '平移' || animation.name === '缩放平移') {
    // 位置计算
    const posFromX = animation.position_from[0] * 100
    const posFromY = animation.position_from[1] * 100
    const posToX = animation.position_to[0] * 100
    const posToY = animation.position_to[1] * 100
    
    const posX = posFromX + (posToX - posFromX) * t
    const posY = posFromY + (posToY - posFromY) * t
    
    const translateX = (50 - posX)
    const translateY = (50 - posY)
    
    if (animation.name === '缩放平移') {
      const scale = animation.scale_from + (animation.scale_to - animation.scale_from) * t
      style.transform = `scale(${scale}) translate(${translateX}%, ${translateY}%)`
    } else {
      style.transform = `translate(${translateX}%, ${translateY}%)`
    }
  }
  
  if (animation.name === '旋转') {
    // 旋转计算
    const rotate = animation.rotate_from + (animation.rotate_to - animation.rotate_from) * t
    style.transform = `rotate(${rotate}deg)`
  }
  
  if (animation.name === '淡入淡出') {
    // 透明度计算
    const opacity = animation.opacity_from + (animation.opacity_to - animation.opacity_from) * t
    style.opacity = opacity
  }
  
  // 应用过渡效果
  style.transition = 'none'
  
  // 设置变换原点
  style.transformOrigin = 'center'
  
  // 应用样式
  previewImageStyle.value = style
}

// 播放预览
const playPreview = () => {
  // 清除可能存在的定时器
  if (previewTimer) {
    clearInterval(previewTimer)
  }
  
  // 重置进度
  previewProgress.value = 0
  
  // 设置过渡效果
  const animation = selectedImage.value.animation
  const easing = animation.easing || 'linear'
  const duration = selectedImage.value.duration || 3
  
  // 计算过渡样式
  let easingFunction = 'linear'
  switch (easing) {
    case 'easeIn':
      easingFunction = 'cubic-bezier(0.42, 0, 1.0, 1.0)'
      break
    case 'easeOut':
      easingFunction = 'cubic-bezier(0, 0, 0.58, 1.0)'
      break
    case 'easeInOut':
      easingFunction = 'cubic-bezier(0.42, 0, 0.58, 1.0)'
      break
  }
  
  // 应用起始样式
  updatePreview(0)
  
  // 使用requestAnimationFrame播放动画
  const startTime = Date.now()
  const animateDuration = duration * 1000 // 转换为毫秒
  
  const animate = () => {
    const currentTime = Date.now()
    const elapsed = currentTime - startTime
    
    if (elapsed >= animateDuration) {
      // 动画结束
      previewProgress.value = 100
      updatePreview(100)
      return
    }
    
    // 计算当前进度
    const progress = (elapsed / animateDuration) * 100
    previewProgress.value = progress
    
    // 应用样式，但使用CSS过渡
    const style = { ...previewImageStyle.value }
    style.transition = `all ${duration}s ${easingFunction}`
    previewImageStyle.value = style
    
    // 继续下一帧
    requestAnimationFrame(animate)
  }
  
  // 开始动画
  requestAnimationFrame(animate)
}

// 重置预览
const resetPreview = () => {
  if (previewTimer) {
    clearInterval(previewTimer)
    previewTimer = null
  }
  
  previewProgress.value = 0
  updatePreview(0)
}

// 初始化组件时添加动画属性
onMounted(() => {
  videoStore.clearError()
  
  // 初始化动画属性
  videoImages.value.forEach(image => {
    // 确保所有必要的动画属性存在
    if (!image.animation) {
      image.animation = {
        name: '缩放',
        scale_from: 1.0,
        scale_to: 1.2,
        position_from: [0.5, 0.5],
        position_to: [0.5, 0.5],
        easing: 'linear'
      }
    }
    
    // 确保有缓动属性
    if (!image.animation.easing) {
      image.animation.easing = 'linear'
    }
    
    if (image.animation.name === '旋转' && !image.animation.rotate_from) {
      image.animation.rotate_from = 0
      image.animation.rotate_to = 360
    }
    
    if (image.animation.name === '淡入淡出' && !image.animation.opacity_from) {
      image.animation.opacity_from = 0
      image.animation.opacity_to = 1
    }
    
    // 初始化已选择的音频
    if (image.audio_path) {
      selectedAudioId[image.id] = image.audio_path
    }
  })
})
</script>

<style scoped>
.creator-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.panel {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 20px;
}

.panel-title {
  font-size: 18px;
  margin-bottom: 15px;
  color: #303133;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.image-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.image-item {
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  padding: 8px;
  transition: all 0.3s;
}

.image-item:hover {
  background-color: #f2f6fc;
}

.image-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.image-thumbnail {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.image-caption {
  margin-top: 8px;
  font-size: 12px;
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-actions {
  margin-top: 8px;
  text-align: center;
}

.timeline {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px 0;
}

.timeline-item {
  margin-bottom: 15px;
  border: 1px solid #ebeef5;
  transition: all 0.3s;
}

.timeline-item.active {
  border-color: #409eff;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.2);
}

.timeline-item-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.timeline-item-index {
  font-size: 16px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  margin-right: 10px;
}

.timeline-item-thumb {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 10px;
}

.timeline-item-body {
  padding: 10px 0;
}

.timeline-item-settings {
  margin-left: 34px;
}

.animation-settings {
  margin-top: 20px;
}

.animation-settings h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #606266;
}

.create-actions {
  margin-top: 20px;
  text-align: center;
}

.help-text {
  margin-top: 10px;
  color: #909399;
  font-size: 14px;
}

.w-full {
  width: 100%;
}

.text-actions {
  margin-top: 10px;
  text-align: right;
}

.preview-container {
  position: relative;
  width: 100%;
  height: 200px;
  margin-bottom: 10px;
}

.preview-target {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-buttons {
  margin-left: 10px;
}
</style> 