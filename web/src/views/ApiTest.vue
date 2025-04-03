<template>
  <div class="api-test-container">
    <el-row :gutter="20">
      <!-- 左侧面板：API列表 -->
      <el-col :span="8">
        <div class="panel">
          <h2 class="panel-title">API列表</h2>
          <ApiList @select="handleSelectApi" />
        </div>
      </el-col>

      <!-- 右侧面板：请求构建器和响应查看器 -->
      <el-col :span="16">
        <div class="panel">
          <h2 class="panel-title">请求构建器</h2>
          <RequestBuilder
            @send-request="handleSendRequest"
            ref="requestBuilder"
          />
        </div>
        
        <div class="panel" v-if="currentResponse">
          <h2 class="panel-title">响应结果</h2>
          <ResponseViewer :response="currentResponse" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import RequestBuilder from '../components/api-test/RequestBuilder.vue'
import ResponseViewer from '../components/api-test/ResponseViewer.vue'
import ApiList from '../components/ApiList.vue'
import axios from 'axios'

// 响应数据
const currentResponse = ref(null)
// 请求构建器引用
const requestBuilder = ref(null)

// 处理选择API
const handleSelectApi = (api) => {
  // 重置请求构建器
  requestBuilder.value?.resetForm()
  // 设置API信息
  requestBuilder.value?.setApiInfo({
    method: api.method,
    endpoint: api.path,
    params: api.params
  })
}

// 处理发送请求
const handleSendRequest = async (requestData) => {
  const startTime = Date.now()
  
  try {
    // 构建请求URL（添加query参数）
    let url = requestData.endpoint
    if (Object.keys(requestData.queryParams).length > 0) {
      const params = new URLSearchParams(requestData.queryParams)
      url += `?${params.toString()}`
    }

    // 发送请求
    const response = await axios({
      method: requestData.method,
      url,
      headers: requestData.headers,
      data: requestData.body
    })

    // 计算响应时间
    const endTime = Date.now()
    const responseTime = endTime - startTime

    // 更新响应数据
    currentResponse.value = {
      status: response.status,
      headers: response.headers,
      data: response.data,
      time: responseTime
    }

    ElMessage.success('请求成功')
  } catch (error) {
    const endTime = Date.now()
    const responseTime = endTime - startTime

    // 更新错误响应
    currentResponse.value = {
      status: error.response?.status || 500,
      headers: error.response?.headers || {},
      data: error.response?.data || { error: error.message },
      time: responseTime
    }

    ElMessage.error(error.message)
  }
}
</script>

<style scoped>
.api-test-container {
  padding: 20px;
  height: calc(100vh - 100px);
  overflow-y: auto;
}

.panel {
  background-color: #fff;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.panel-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}
</style> 