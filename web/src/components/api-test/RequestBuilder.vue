<template>
  <div class="request-builder">
    <el-form :model="requestForm" label-width="100px">
      <!-- 请求方法选择 -->
      <el-form-item label="请求方法">
        <el-select v-model="requestForm.method" class="method-select">
          <el-option v-for="method in methods" :key="method" :label="method" :value="method" />
        </el-select>
      </el-form-item>

      <!-- API端点输入 -->
      <el-form-item label="API端点">
        <el-input v-model="requestForm.endpoint" placeholder="/api/..." />
      </el-form-item>

      <!-- 请求头部 -->
      <el-form-item label="请求头">
        <div v-for="(header, index) in requestForm.headers" :key="index" class="header-item">
          <el-input v-model="header.key" placeholder="Header Key" class="header-key" />
          <el-input v-model="header.value" placeholder="Header Value" class="header-value" />
          <el-button type="danger" :icon="Delete" circle @click="removeHeader(index)" />
        </div>
        <el-button type="primary" plain @click="addHeader">添加请求头</el-button>
      </el-form-item>

      <!-- 请求参数 -->
      <el-form-item label="请求参数">
        <el-tabs v-model="paramType">
          <el-tab-pane label="Query参数" name="query">
            <div v-for="(param, index) in requestForm.queryParams" :key="index" class="param-item">
              <el-input v-model="param.key" placeholder="参数名" class="param-key" />
              <el-input v-model="param.value" placeholder="参数值" class="param-value" />
              <el-button type="danger" :icon="Delete" circle @click="removeQueryParam(index)" />
            </div>
            <el-button type="primary" plain @click="addQueryParam">添加参数</el-button>
          </el-tab-pane>
          
          <el-tab-pane label="请求体" name="body" v-if="showRequestBody">
            <el-radio-group v-model="requestForm.bodyType" class="body-type-group">
              <el-radio label="json">JSON</el-radio>
              <el-radio label="form-data">Form Data</el-radio>
            </el-radio-group>
            
            <div v-if="requestForm.bodyType === 'json'" class="json-editor">
              <el-input
                v-model="requestForm.jsonBody"
                type="textarea"
                :rows="5"
                placeholder="{ }"
                resize="both"
                class="json-textarea"
              />
            </div>
            
            <div v-else class="form-data">
              <div v-for="(param, index) in requestForm.formData" :key="index" class="param-item">
                <el-input v-model="param.key" placeholder="字段名" class="param-key" />
                <el-input v-model="param.value" placeholder="字段值" class="param-value" />
                <el-button type="danger" :icon="Delete" circle @click="removeFormData(index)" />
              </div>
              <el-button type="primary" plain @click="addFormData">添加字段</el-button>
            </div>
            
            <!-- 参数说明（可折叠） -->
            <el-collapse v-if="currentApiParams" class="param-hints">
              <el-collapse-item title="参数说明">
                <el-descriptions :column="1" border>
                  <el-descriptions-item 
                    v-for="(param, key) in currentApiParams" 
                    :key="key"
                    :label="key"
                  >
                    <div class="param-description">
                      <div>类型：{{ param.type || param }}</div>
                      <div v-if="param.description">说明：{{ param.description }}</div>
                      <el-tag 
                        :type="param.required ? 'danger' : 'info'"
                        size="small"
                      >
                        {{ param.required ? '必填' : '选填' }}
                      </el-tag>
                    </div>
                  </el-descriptions-item>
                </el-descriptions>
              </el-collapse-item>
            </el-collapse>
          </el-tab-pane>
        </el-tabs>
      </el-form-item>

      <!-- 发送按钮 -->
      <el-form-item>
        <el-button type="primary" @click="sendRequest">发送请求</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'

const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

const requestForm = ref({
  method: 'GET',
  endpoint: '',
  headers: [],
  queryParams: [],
  formData: [],
  bodyType: 'json',
  jsonBody: ''
})

const paramType = ref('query')
const currentApiParams = ref(null)

// 计算属性
const showRequestBody = computed(() => {
  return ['POST', 'PUT', 'PATCH'].includes(requestForm.value.method)
})

// 监听API参数变化，自动生成query参数输入行
watch(() => currentApiParams.value?.query, (newParams) => {
  if (newParams) {
    requestForm.value.queryParams = Object.entries(newParams).map(([key, param]) => ({
      key,
      value: '',
      required: param.required !== undefined ? param.required : !param.includes('?')
    }))
  }
}, { immediate: true })

// 方法
const addHeader = () => {
  requestForm.value.headers.push({ key: '', value: '' })
}

const removeHeader = (index) => {
  requestForm.value.headers.splice(index, 1)
}

const addQueryParam = () => {
  requestForm.value.queryParams.push({ key: '', value: '' })
}

const removeQueryParam = (index) => {
  requestForm.value.queryParams.splice(index, 1)
}

const addFormData = () => {
  requestForm.value.formData.push({ key: '', value: '' })
}

const removeFormData = (index) => {
  requestForm.value.formData.splice(index, 1)
}

const resetForm = () => {
  requestForm.value = {
    method: 'GET',
    endpoint: '',
    headers: [],
    queryParams: [],
    formData: [],
    bodyType: 'json',
    jsonBody: ''
  }
  currentApiParams.value = null
}

// 设置API信息
const setApiInfo = (api) => {
  requestForm.value.method = api.method
  requestForm.value.endpoint = api.endpoint
  currentApiParams.value = api.params

  // 清空现有参数
  requestForm.value.headers = []
  requestForm.value.queryParams = []
  requestForm.value.formData = []
  requestForm.value.jsonBody = ''

  // 设置请求体
  if (api.params?.body) {
    requestForm.value.bodyType = 'json'
    requestForm.value.jsonBody = JSON.stringify(
      Object.fromEntries(
        Object.entries(api.params.body).map(([key, param]) => [
          key,
          param.type === 'File' ? null : ''
        ])
      ),
      null,
      2
    )
  }
}

const sendRequest = () => {
  // 构建请求数据
  const requestData = {
    method: requestForm.value.method,
    endpoint: requestForm.value.endpoint,
    headers: Object.fromEntries(
      requestForm.value.headers
        .filter(h => h.key && h.value)
        .map(h => [h.key, h.value])
    ),
    queryParams: Object.fromEntries(
      requestForm.value.queryParams
        .filter(p => p.key && p.value)
        .map(p => [p.key, p.value])
    )
  }

  if (showRequestBody.value) {
    if (requestForm.value.bodyType === 'json') {
      try {
        requestData.body = JSON.parse(requestForm.value.jsonBody)
      } catch (e) {
        ElMessage.error('JSON格式错误')
        return
      }
    } else {
      requestData.body = Object.fromEntries(
        requestForm.value.formData
          .filter(f => f.key && f.value)
          .map(f => [f.key, f.value])
      )
    }
  }

  // 发送请求事件
  emit('send-request', requestData)
}

// 定义事件和方法
const emit = defineEmits(['send-request'])
defineExpose({ resetForm, setApiInfo })
</script>

<style scoped>
.request-builder {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.method-select {
  width: 120px;
}

.header-item,
.param-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.header-key,
.param-key {
  width: 200px;
}

.header-value,
.param-value {
  flex: 1;
}

.body-type-group {
  margin-bottom: 15px;
}

.json-editor {
  margin-bottom: 15px;
}

.json-textarea {
  width: 100%;
  font-family: monospace;
}

:deep(.el-textarea__inner) {
  font-family: monospace;
  min-height: 120px !important;
}

.param-hints {
  margin-top: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.param-description {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

:deep(.el-descriptions__cell) {
  padding: 12px 16px;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
  color: #303133;
  width: 150px;
}
</style> 