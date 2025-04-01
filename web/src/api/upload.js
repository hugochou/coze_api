import request from '../utils/request'

/**
 * 上传图片
 * @param {File} file - 图片文件
 * @returns {Promise} - 返回上传结果
 */
export function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/upload/image',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 上传音频
 * @param {File} file - 音频文件
 * @returns {Promise} - 返回上传结果
 */
export function uploadAudio(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/upload/audio',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 获取文件完整URL
 * @param {string} path - 文件相对路径
 * @returns {string} - 完整URL
 */
export function getFileUrl(path) {
  if (!path) return ''
  
  // 如果已经是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // 否则拼接基础URL
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
  // 确保path以/开头
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  
  return `${baseUrl}${normalizedPath}`
} 