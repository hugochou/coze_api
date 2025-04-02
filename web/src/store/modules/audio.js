import { defineStore } from 'pinia'
import { audio } from '../../api'

export const useAudioStore = defineStore('audio', {
  state: () => ({
    // 创建的音频列表
    createdAudios: [],
    // 当前选中的音频
    selectedAudio: null,
    // 音频参数配置
    audioConfig: {
      voice: 'zh-CN',
      speed: 1.0,
      format: 'mp3'
    },
    // 创建状态
    creating: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    // 获取音频列表
    audios: (state) => state.createdAudios,
    
    // 获取音频配置
    config: (state) => state.audioConfig
  },
  
  actions: {
    // 创建音频
    async createAudio(data) {
      try {
        this.creating = true
        this.error = null
        
        // 应用默认配置
        const params = {
          ...this.audioConfig,
          ...data
        }
        
        const result = await audio.createAudio(params)
        
        // 添加到创建的音频列表
        if (result) {
          this.createdAudios.push({
            id: Date.now().toString(),
            text: data.text,
            params: { ...params },
            ...result
          })
        }
        
        return result
      } catch (error) {
        console.error('创建音频失败:', error)
        this.error = error.message || '创建音频失败'
        throw error
      } finally {
        this.creating = false
      }
    },
    
    // 选择音频
    selectAudio(audioItem) {
      this.selectedAudio = audioItem
    },
    
    // 删除创建的音频
    deleteAudio(id) {
      this.createdAudios = this.createdAudios.filter(audio => audio.id !== id)
      
      if (this.selectedAudio && this.selectedAudio.id === id) {
        this.selectedAudio = null
      }
    },
    
    // 更新音频配置
    updateConfig(config) {
      this.audioConfig = {
        ...this.audioConfig,
        ...config
      }
    },
    
    // 清空错误信息
    clearError() {
      this.error = null
    }
  }
}) 