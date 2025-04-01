import { defineStore } from 'pinia'
import { video } from '../../api'

export const useVideoStore = defineStore('video', {
  state: () => ({
    // 视频列表
    videos: [],
    // 选中的视频
    selectedVideo: null,
    // 视频创建配置
    videoConfig: {
      transition: '淡入淡出',
      transition_duration: 0.7,
      output_fps: 30,
      output_quality: 'medium'
    },
    // 视频创建图片列表
    videoImages: [],
    // 加载状态
    loading: false,
    // 创建中状态
    creating: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    // 获取视频列表
    videoList: (state) => state.videos,
    
    // 获取选中的视频
    currentVideo: (state) => state.selectedVideo,
    
    // 获取视频配置
    config: (state) => state.videoConfig,
    
    // 获取视频创建图片数量
    imageCount: (state) => state.videoImages.length,
    
    // 检查是否可以创建视频
    canCreateVideo: (state) => state.videoImages.length > 0
  },
  
  actions: {
    // 获取视频列表
    async fetchVideos() {
      try {
        this.loading = true
        this.error = null
        
        const result = await video.getVideoList()
        
        if (result && result.videos) {
          this.videos = result.videos
        }
        
        return result
      } catch (error) {
        console.error('获取视频列表失败:', error)
        this.error = error.message || '获取视频列表失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 选择视频
    selectVideo(videoItem) {
      this.selectedVideo = videoItem
    },
    
    // 添加图片到视频创建列表
    addImageToVideo(imageItem) {
      // 根据后端要求格式化图片项
      const newItem = {
        id: imageItem.id || Date.now().toString(),
        image_path: imageItem.path || imageItem.image_path,
        text: imageItem.text || '',
        duration: 3,  // 默认3秒
        animation: {
          name: '缩放',
          scale_from: 1.0,
          scale_to: 1.2,
          position_from: [0.5, 0.5],
          position_to: [0.5, 0.5]
        },
        audio_path: null,
        order: this.videoImages.length
      }
      
      this.videoImages.push(newItem)
      return newItem
    },
    
    // 移除视频创建列表中的图片
    removeImageFromVideo(id) {
      this.videoImages = this.videoImages.filter(img => img.id !== id)
      
      // 重新排序
      this.videoImages.forEach((img, index) => {
        img.order = index
      })
    },
    
    // 更新视频创建列表中的图片
    updateVideoImage(id, updates) {
      const index = this.videoImages.findIndex(img => img.id === id)
      if (index !== -1) {
        this.videoImages[index] = {
          ...this.videoImages[index],
          ...updates
        }
      }
    },
    
    // 为视频图片添加音频
    setImageAudio(imageId, audioPath) {
      const index = this.videoImages.findIndex(img => img.id === imageId)
      if (index !== -1) {
        this.videoImages[index].audio_path = audioPath
      }
    },
    
    // 重新排序视频图片
    reorderVideoImages(newOrder) {
      // newOrder是包含id的数组，按新顺序重排
      const reordered = []
      
      newOrder.forEach((id, index) => {
        const image = this.videoImages.find(img => img.id === id)
        if (image) {
          reordered.push({
            ...image,
            order: index
          })
        }
      })
      
      this.videoImages = reordered
    },
    
    // 更新视频配置
    updateVideoConfig(config) {
      this.videoConfig = {
        ...this.videoConfig,
        ...config
      }
    },
    
    // 创建视频
    async createVideo() {
      if (this.videoImages.length === 0) {
        this.error = '请至少添加一张图片'
        return null
      }
      
      try {
        this.creating = true
        this.error = null
        
        // 准备请求数据
        const requestData = {
          images: this.videoImages,
          ...this.videoConfig
        }
        
        const result = await video.createVideo(requestData)
        
        // 创建成功后刷新视频列表
        await this.fetchVideos()
        
        // 选择新创建的视频
        if (result && result.video_path) {
          const newVideo = this.videos.find(v => v.path === result.video_path)
          if (newVideo) {
            this.selectVideo(newVideo)
          }
        }
        
        return result
      } catch (error) {
        console.error('创建视频失败:', error)
        this.error = error.message || '创建视频失败'
        throw error
      } finally {
        this.creating = false
      }
    },
    
    // 清空错误信息
    clearError() {
      this.error = null
    },
    
    // 重置视频创建状态
    resetVideoCreation() {
      this.videoImages = []
      this.error = null
    }
  }
}) 