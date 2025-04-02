import { defineStore } from 'pinia'
import { file } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

export const useFileStore = defineStore('file', {
  state: () => ({
    // 文件列表
    files: [],
    // 选中的文件列表
    selectedFiles: [],
    // 选中文件的预览
    previewFile: null,
    // 预览对话框是否可见
    previewVisible: false,
    // 加载状态
    loading: false,
    // 当前筛选类型
    currentType: 'all',
    // 错误信息
    error: null
  }),
  
  getters: {
    // 获取特定类型的文件数量
    fileCount: (state) => {
      const counts = {
        all: state.files.length,
        image: state.files.filter(f => f.type === 'image').length,
        audio: state.files.filter(f => f.type === 'audio').length,
        video: state.files.filter(f => f.type === 'video').length
      }
      return counts
    },
    
    // 是否有选中的文件
    hasSelected: (state) => state.selectedFiles.length > 0,
    
    // 获取选中的文件数量
    selectedCount: (state) => state.selectedFiles.length,
    
    // 获取分组后的文件列表（按日期分组）
    groupedFiles: (state) => {
      const groups = {}
      
      state.files.forEach(file => {
        // 提取日期部分
        const date = file.modified.split(' ')[0]
        
        if (!groups[date]) {
          groups[date] = []
        }
        
        groups[date].push(file)
      })
      
      // 转换为数组格式，便于渲染
      return Object.keys(groups).sort().reverse().map(date => ({
        date,
        files: groups[date]
      }))
    }
  },
  
  actions: {
    // 加载文件列表
    async fetchFiles(type = 'all') {
      try {
        this.loading = true
        this.currentType = type
        this.error = null
        this.selectedFiles = []
        
        const response = await file.getFileList(type)
        
        if (response && response.success) {
          this.files = response.files || []
        } else {
          throw new Error(response.error || '获取文件列表失败')
        }
      } catch (error) {
        console.error('获取文件列表失败:', error)
        this.error = error.message || '获取文件列表失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 选择/取消选择文件
    toggleSelectFile(fileItem) {
      const index = this.selectedFiles.findIndex(f => f.path === fileItem.path)
      
      if (index >= 0) {
        // 已选中，则取消选择
        this.selectedFiles.splice(index, 1)
      } else {
        // 未选中，则添加到选中列表
        this.selectedFiles.push(fileItem)
      }
    },
    
    // 检查文件是否被选中
    isSelected(fileItem) {
      return this.selectedFiles.some(f => f.path === fileItem.path)
    },
    
    // 全选/取消全选
    toggleSelectAll(selected) {
      if (selected) {
        // 全选当前类型的文件
        this.selectedFiles = [...this.files]
      } else {
        // 取消全选
        this.selectedFiles = []
      }
    },
    
    // 预览文件
    openPreviewFile(fileItem) {
      this.previewFile = fileItem
      this.previewVisible = true
    },
    
    // 关闭预览
    closePreview() {
      this.previewVisible = false
      this.previewFile = null
    },
    
    // 删除选中的文件
    async deleteSelectedFiles() {
      try {
        if (this.selectedFiles.length === 0) {
          return
        }
        
        // 二次确认
        await ElMessageBox.confirm(
          `确定要删除选中的 ${this.selectedFiles.length} 个文件吗？此操作不可恢复。`,
          '删除确认',
          {
            confirmButtonText: '确定删除',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const filePaths = this.selectedFiles.map(f => f.path)
        
        const response = await file.deleteFiles(filePaths)
        
        if (response && response.success) {
          ElMessage.success(`成功删除 ${response.deleted} 个文件`)
          
          // 如果有删除失败的文件
          if (response.failed && response.failed.length > 0) {
            ElMessage.warning(`${response.failed.length} 个文件删除失败`)
          }
          
          // 重新加载文件列表
          await this.fetchFiles(this.currentType)
        } else {
          throw new Error(response.error || '删除文件失败')
        }
      } catch (error) {
        // 如果是用户取消操作，不显示错误
        if (error === 'cancel' || error.toString().includes('cancel')) {
          return
        }
        
        console.error('删除文件失败:', error)
        ElMessage.error(error.message || '删除文件失败')
      }
    },
    
    // 清空指定类型的文件
    async clearFiles(type = 'all') {
      try {
        // 二次确认
        const typeText = type === 'all' ? '所有' : (
          type === 'image' ? '图片' : (
            type === 'audio' ? '音频' : '视频'
          )
        )
        
        await ElMessageBox.confirm(
          `确定要删除${typeText}文件吗？此操作不可恢复。`,
          '清空确认',
          {
            confirmButtonText: '确定清空',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await file.clearFiles(type)
        
        if (response && response.success) {
          ElMessage.success(response.message || `成功清空${typeText}文件`)
          
          // 重新加载文件列表
          await this.fetchFiles(this.currentType)
        } else {
          throw new Error(response.error || '清空文件失败')
        }
      } catch (error) {
        // 如果是用户取消操作，不显示错误
        if (error === 'cancel' || error.toString().includes('cancel')) {
          return
        }
        
        console.error('清空文件失败:', error)
        ElMessage.error(error.message || '清空文件失败')
      }
    }
  }
}) 