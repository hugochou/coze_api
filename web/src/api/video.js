import request from '../utils/request'

/**
 * 创建视频
 * @param {Object} data - 创建视频所需参数
 * @param {Array} data.images - 图片项列表
 * @param {string} data.transition - 转场效果
 * @param {number} data.transition_duration - 转场时长
 * @param {number} data.output_fps - 输出帧率
 * @param {string} data.output_quality - 输出质量
 * @returns {Promise} - 返回创建结果
 */
export function createVideo(data) {
  return request({
    url: '/api/video/create',
    method: 'post',
    data
  })
}

/**
 * 获取视频列表
 * @returns {Promise} - 返回视频列表
 */
export function getVideoList() {
  return request({
    url: '/api/video/list',
    method: 'get'
  })
}

/**
 * 获取视频URL
 * @param {string} filename - 视频文件名
 * @returns {string} - 视频URL
 */
export function getVideoUrl(filename) {
  if (!filename) return ''
  
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
  return `${baseUrl}/videos/${filename}`
}

/**
 * 下载视频
 * @param {string} filename - 视频文件名
 */
export function downloadVideo(filename) {
  const url = getVideoUrl(filename)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
} 