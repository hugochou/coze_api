import request from '../utils/request'

/**
 * 获取文件列表
 * @param {string} [type='all'] - 文件类型，可选值为 all, image, audio, video
 * @returns {Promise} - 返回文件列表
 */
export function getFileList(type = 'all') {
  return request({
    url: '/api/file/list',
    method: 'get',
    params: { type }
  })
}

/**
 * 删除文件
 * @param {Array} files - 要删除的文件路径列表
 * @returns {Promise} - 返回删除结果
 */
export function deleteFiles(files) {
  return request({
    url: '/api/file/delete',
    method: 'post',
    data: { files }
  })
}

/**
 * 清空文件
 * @param {string} type - 文件类型，可选值为 all, image, audio, video
 * @returns {Promise} - 返回清空结果
 */
export function clearFiles(type) {
  return request({
    url: '/api/file/clear',
    method: 'post',
    data: { type }
  })
}

/**
 * 获取文件URL
 * @param {string} path - 文件路径或URL
 * @returns {string} - 完整的文件URL
 */
export function getFileUrl(path) {
  if (!path) return ''
  
  // 如果是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // 如果是相对路径，拼接API基础URL
  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
  return `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}`
}

/**
 * 获取文件图标
 * @param {string} fileType - 文件类型
 * @param {string} fileName - 文件名
 * @returns {string} - 图标名称
 */
export function getFileIcon(fileType, fileName) {
  if (fileType === 'image') {
    return 'Picture'
  }
  
  if (fileType === 'audio') {
    return 'Microphone'
  }
  
  if (fileType === 'video') {
    return 'VideoPlay'
  }
  
  // 根据扩展名进一步判断
  const ext = fileName.split('.').pop().toLowerCase()
  
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'].includes(ext)) {
    return 'Picture'
  }
  
  if (['mp3', 'wav', 'ogg', 'm4a'].includes(ext)) {
    return 'Microphone'
  }
  
  if (['mp4', 'webm', 'mov', 'avi'].includes(ext)) {
    return 'VideoPlay'
  }
  
  return 'Document'
}

/**
 * 格式化文件大小
 * @param {number} size - 文件大小（字节）
 * @returns {string} - 格式化后的文件大小
 */
export function formatFileSize(size) {
  if (size < 1024) {
    return size + ' B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  } else if (size < 1024 * 1024 * 1024) {
    return (size / (1024 * 1024)).toFixed(2) + ' MB'
  } else {
    return (size / (1024 * 1024 * 1024)).toFixed(2) + ' GB'
  }
} 