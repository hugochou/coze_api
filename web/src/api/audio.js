import request from '../utils/request'

/**
 * 创建音频（文本转语音）
 * @param {Object} data - 创建音频所需参数
 * @param {string} data.text - 要转换的文本内容
 * @param {string} [data.voice='zh-CN'] - 语音类型
 * @param {number} [data.speed=1.0] - 语速 (0.5-2.0)
 * @param {string} [data.format='mp3'] - 输出格式 (mp3, wav)
 * @returns {Promise} - 返回创建结果
 */
export function createAudio(data) {
  return request({
    url: '/api/audio/create',
    method: 'post',
    data
  })
}

/**
 * 获取音频URL
 * @param {string} filename - 音频文件名或路径
 * @returns {string} - 音频URL
 */
export function getAudioUrl(filename) {
  if (!filename) return ''
  
  // 如果已经是完整URL，直接返回
  if (filename.startsWith('http://') || filename.startsWith('https://')) {
    return filename
  }
  
  // 如果是相对路径但不以/uploads开头，添加前缀
  let path = filename
  if (!path.startsWith('/uploads') && !path.startsWith('uploads')) {
    path = `/uploads/${path.replace(/^\//, '')}`
  }
  
  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
  return `${baseUrl}${path}`
} 