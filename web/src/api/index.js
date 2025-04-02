import request from '../utils/request'
import * as upload from './upload'
import * as video from './video'
import * as audio from './audio'
import * as file from './file'

/**
 * 获取API健康状态
 * @returns {Promise} - 返回健康状态信息
 */
export function getHealthStatus() {
  return request({
    url: '/api/health',
    method: 'get'
  })
}

// 导出API模块
export {
  upload,
  video,
  audio,
  file
}

// 统一导出
export default {
  upload,
  video,
  audio,
  file,
  getHealthStatus
} 