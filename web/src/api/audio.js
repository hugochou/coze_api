import request from '../utils/request'

/**
 * 创建音频（文本转语音）
 * @param {Object} data - 音频创建参数
 * @param {string} data.text - 要转换为音频的文本
 * @param {string} [data.voice] - 语音类型
 * @param {number} [data.speed] - 语速（0.5-2.0）
 * @param {string} [data.format] - 输出格式（mp3, wav）
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
 * @param {string} path - 音频文件路径
 * @returns {string} - 音频URL
 */
export function getAudioUrl(path) {
  if (!path) return ''
  
  // 如果是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // 如果是相对路径，拼接API基础URL
  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
  return `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}`
} 