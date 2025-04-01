import request from '../utils/request'
import * as uploadApi from './upload'
import * as videoApi from './video'
import * as audioApi from './audio'

/**
 * 获取API服务健康状态
 * @returns {Promise} - 返回健康状态信息
 */
export function getHealthStatus() {
  return request({
    url: '/api/health',
    method: 'get'
  })
}

// 导出所有API
export const upload = uploadApi
export const video = videoApi
export const audio = audioApi

// 统一导出
export default {
  ...uploadApi,
  ...videoApi,
  ...audioApi,
  getHealthStatus
} 