<template>
  <div class="audio-creator-container">
    <h2 class="page-title">音频创建</h2>
    
    <el-row :gutter="20">
      <!-- 左侧：文本编辑和参数控制面板 -->
      <el-col :span="16">
        <div class="panel">
          <h3 class="panel-title">文本转音频</h3>
          
          <el-form :model="audioForm" label-position="top">
            <el-form-item label="输入文本">
              <el-input
                v-model="audioForm.text"
                type="textarea"
                :rows="8"
                placeholder="请输入要转换为音频的文本内容"
                resize="none"
              />
              <div class="text-stats">
                <span>{{ textLength }} 个字符</span>
                <span>预计 {{ estimatedDuration }} 秒</span>
              </div>
            </el-form-item>
            
            <el-divider>语音参数设置</el-divider>
            
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="语音类型">
                  <el-select v-model="audioForm.voice" class="w-full">
                    <el-option label="普通话(女声)" value="zh-CN-female" />
                    <el-option label="普通话(男声)" value="zh-CN-male" />
                    <el-option label="英语(女声)" value="en-US-female" />
                    <el-option label="英语(男声)" value="en-US-male" />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="8">
                <el-form-item label="语速">
                  <el-slider
                    v-model="audioForm.speed"
                    :min="0.5"
                    :max="2"
                    :step="0.1"
                    show-input
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="8">
                <el-form-item label="输出格式">
                  <el-radio-group v-model="audioForm.format">
                    <el-radio label="mp3">MP3</el-radio>
                    <el-radio label="wav">WAV</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item>
              <div class="form-actions">
                <el-button 
                  type="primary" 
                  :disabled="!audioForm.text" 
                  :loading="creating" 
                  @click="createAudio"
                >
                  生成音频
                </el-button>
                <el-button 
                  @click="resetForm"
                >
                  重置
                </el-button>
              </div>
            </el-form-item>
          </el-form>
        </div>
        
        <!-- 常用文本模板 -->
        <div class="panel">
          <div class="panel-header">
            <h3 class="panel-title">常用文本模板</h3>
            <el-button 
              type="primary" 
              size="small" 
              plain
              @click="showNewTemplateDialog = true"
            >
              添加模板
            </el-button>
          </div>
          
          <div class="templates-list">
            <div 
              v-for="(template, index) in textTemplates" 
              :key="index"
              class="template-item"
            >
              <div class="template-content">{{ template }}</div>
              <div class="template-actions">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="useTemplate(template)"
                >
                  使用
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="removeTemplate(index)"
                >
                  删除
                </el-button>
              </div>
            </div>
            
            <el-empty 
              v-if="!textTemplates.length" 
              description="暂无文本模板，点击添加模板按钮创建" 
            />
          </div>
        </div>
      </el-col>
      
      <!-- 右侧：已创建音频列表 -->
      <el-col :span="8">
        <div class="panel">
          <h3 class="panel-title">已创建音频</h3>
          
          <div class="audios-list" v-loading="loading">
            <el-empty 
              description="暂无已创建的音频" 
              v-if="!createdAudios.length && !loading" 
            />
            
            <div 
              v-for="(audioItem, index) in createdAudios" 
              :key="audioItem.id"
              class="audio-item"
            >
              <div class="audio-info">
                <div class="audio-text">{{ truncateText(audioItem.text, 30) }}</div>
                <div class="audio-meta">
                  <span>{{ formatDate(audioItem.createTime || new Date()) }}</span>
                  <span>{{ audioItem.params.voice }}</span>
                  <span>速度: {{ audioItem.params.speed }}</span>
                </div>
              </div>
              
              <div class="audio-player">
                <audio controls :src="getAudioUrl(audioItem)">
                  您的浏览器不支持音频播放
                </audio>
              </div>
              
              <div class="audio-actions">
                <el-button 
                  type="primary" 
                  size="small" 
                  icon="Download"
                  @click="downloadAudio(audioItem)"
                >
                  下载
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  icon="Delete"
                  @click="deleteAudio(audioItem.id)"
                >
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    
    <!-- 新建模板对话框 -->
    <el-dialog
      v-model="showNewTemplateDialog"
      title="添加文本模板"
      width="500px"
    >
      <el-form :model="newTemplate">
        <el-form-item label="模板内容">
          <el-input
            v-model="newTemplate.text"
            type="textarea"
            :rows="4"
            placeholder="请输入文本模板内容"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showNewTemplateDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          :disabled="!newTemplate.text" 
          @click="addTemplate"
        >
          保存
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 错误提示 -->
    <el-dialog
      v-model="showErrorDialog"
      title="操作失败"
      width="400px"
    >
      <p>{{ errorMessage }}</p>
      <template #footer>
        <el-button type="primary" @click="showErrorDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Delete } from '@element-plus/icons-vue'
import { useAudioStore } from '../store/modules/audio'
import { audio } from '../api'

const audioStore = useAudioStore()

// 表单数据
const audioForm = ref({
  text: '',
  voice: 'zh-CN-female',
  speed: 1.0,
  format: 'mp3'
})

// 状态变量
const creating = computed(() => audioStore.creating)
const loading = ref(false)
const showNewTemplateDialog = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')
const newTemplate = ref({ text: '' })

// 文本模板 (使用localStorage存储)
const textTemplates = ref([
  '这是一段示例文本，用于测试文本转语音功能。',
  '欢迎使用Coze API的文本转语音服务，您可以通过此功能将文本转换为自然流畅的语音。',
  '图片转视频服务已经准备就绪，现在您可以添加生动的配音了。'
])

// 计算属性
const textLength = computed(() => {
  return audioForm.value.text ? audioForm.value.text.length : 0
})

const estimatedDuration = computed(() => {
  // 简单估算：中文每分钟约300字，英文每分钟约150词
  const isChineseVoice = audioForm.value.voice.startsWith('zh')
  const charsPerSecond = isChineseVoice ? 5 : 2.5
  const duration = Math.ceil(textLength.value / charsPerSecond)
  // 考虑语速因素
  return Math.ceil(duration / audioForm.value.speed)
})

// 获取创建的音频
const createdAudios = computed(() => {
  return audioStore.audios || []
})

// 获取音频URL
const getAudioUrl = (audioItem) => {
  return audioItem.full_url || audio.getAudioUrl(audioItem.url || audioItem.path)
}

// 创建音频
const createAudio = async () => {
  if (!audioForm.value.text) {
    ElMessage.warning('请输入要转换的文本内容')
    return
  }
  
  try {
    const result = await audioStore.createAudio({
      text: audioForm.value.text,
      voice: audioForm.value.voice,
      speed: audioForm.value.speed,
      format: audioForm.value.format
    })
    
    if (result) {
      ElMessage.success('音频创建成功')
      
      // 保存当前文本到模板
      saveTextAsTemplate()
    }
  } catch (error) {
    console.error('创建音频失败:', error)
    errorMessage.value = error.message || '创建音频失败'
    showErrorDialog.value = true
  }
}

// 重置表单
const resetForm = () => {
  audioForm.value = {
    text: '',
    voice: 'zh-CN-female',
    speed: 1.0,
    format: 'mp3'
  }
}

// 下载音频
const downloadAudio = (audioItem) => {
  const url = getAudioUrl(audioItem)
  const link = document.createElement('a')
  link.href = url
  
  // 生成文件名：取前10个字符作为文件名
  const filename = `audio_${truncateText(audioItem.text, 10).replace(/\s+/g, '_')}.${audioItem.params.format || 'mp3'}`
  
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('正在下载音频')
}

// 删除音频
const deleteAudio = (id) => {
  audioStore.deleteAudio(id)
  ElMessage.success('音频已删除')
}

// 使用模板
const useTemplate = (template) => {
  audioForm.value.text = template
}

// 添加模板
const addTemplate = () => {
  if (!newTemplate.value.text) return
  
  // 检查是否已存在相同模板
  if (!textTemplates.value.includes(newTemplate.value.text)) {
    textTemplates.value.push(newTemplate.value.text)
    saveTemplates()
    ElMessage.success('模板添加成功')
  } else {
    ElMessage.warning('已存在相同的模板')
  }
  
  newTemplate.value.text = ''
  showNewTemplateDialog.value = false
}

// 删除模板
const removeTemplate = (index) => {
  textTemplates.value.splice(index, 1)
  saveTemplates()
  ElMessage.success('模板已删除')
}

// 保存当前文本为模板
const saveTextAsTemplate = () => {
  const text = audioForm.value.text
  if (!text || text.length < 5 || textTemplates.value.includes(text)) return
  
  // 询问是否保存当前文本为模板
  // 这里简化处理，直接保存，不再询问
  if (textTemplates.value.length >= 10) {
    // 如果模板数量过多，移除最早的
    textTemplates.value.shift()
  }
  
  textTemplates.value.push(text)
  saveTemplates()
}

// 保存模板到localStorage
const saveTemplates = () => {
  localStorage.setItem('audioTextTemplates', JSON.stringify(textTemplates.value))
}

// 加载模板
const loadTemplates = () => {
  const savedTemplates = localStorage.getItem('audioTextTemplates')
  if (savedTemplates) {
    try {
      const templates = JSON.parse(savedTemplates)
      if (Array.isArray(templates)) {
        textTemplates.value = templates
      }
    } catch (e) {
      console.error('加载模板失败:', e)
    }
  }
}

// 文本截断
const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  
  if (typeof date === 'string') {
    date = new Date(date)
  }
  
  return date.toLocaleString()
}

// 组件挂载时初始化
onMounted(() => {
  loadTemplates()
  
  // 加载已创建的音频
  loading.value = true
  
  // 简单延迟，模拟加载效果
  setTimeout(() => {
    loading.value = false
  }, 500)
})
</script>

<style scoped>
.audio-creator-container {
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

.text-stats {
  margin-top: 5px;
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 10px;
}

.w-full {
  width: 100%;
}

.templates-list {
  margin-top: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.template-item {
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
}

.template-item:last-child {
  border-bottom: none;
}

.template-content {
  margin-bottom: 10px;
  color: #606266;
}

.template-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.audios-list {
  max-height: 600px;
  overflow-y: auto;
}

.audio-item {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
}

.audio-info {
  margin-bottom: 10px;
}

.audio-text {
  font-size: 14px;
  color: #303133;
  margin-bottom: 5px;
}

.audio-meta {
  font-size: 12px;
  color: #909399;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.audio-player {
  margin: 10px 0;
}

.audio-player audio {
  width: 100%;
}

.audio-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 