import { defineStore } from 'pinia'
import { upload } from '../../api'

export const useUploadStore = defineStore('upload', {
  state: () => ({
    // 已上传的图片列表
    uploadedImages: [],
    // 已上传的音频列表
    uploadedAudios: [],
    // 上传状态
    uploading: false,
    // 上传错误信息
    error: null
  }),
  
  getters: {
    // 获取上传的图片数量
    imageCount: (state) => state.uploadedImages.length,
    
    // 获取上传的音频数量
    audioCount: (state) => state.uploadedAudios.length
  },
  
  actions: {
    // 上传图片
    async uploadImage(file) {
      try {
        this.uploading = true
        this.error = null
        
        const result = await upload.uploadImage(file)
        
        // 添加到已上传列表
        this.uploadedImages.push({
          id: Date.now().toString(),
          originalName: file.name,
          ...result
        })
        
        return result
      } catch (error) {
        console.error('上传图片失败:', error)
        this.error = error.message || '上传图片失败'
        throw error
      } finally {
        this.uploading = false
      }
    },
    
    // 上传音频
    async uploadAudio(file) {
      try {
        this.uploading = true
        this.error = null
        
        const result = await upload.uploadAudio(file)
        
        // 添加到已上传列表
        this.uploadedAudios.push({
          id: Date.now().toString(),
          originalName: file.name,
          ...result
        })
        
        return result
      } catch (error) {
        console.error('上传音频失败:', error)
        this.error = error.message || '上传音频失败'
        throw error
      } finally {
        this.uploading = false
      }
    },
    
    // 删除已上传的图片
    removeUploadedImage(id) {
      this.uploadedImages = this.uploadedImages.filter(image => image.id !== id)
    },
    
    // 删除已上传的音频
    removeUploadedAudio(id) {
      this.uploadedAudios = this.uploadedAudios.filter(audio => audio.id !== id)
    },
    
    // 清空错误信息
    clearError() {
      this.error = null
    }
  }
}) 