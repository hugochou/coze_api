<template>
  <div class="response-viewer">
    <div class="response-header">
      <div class="status" :class="{ 'success': isSuccess }">
        状态码: {{ response.status }}
      </div>
      <div class="time">
        响应时间: {{ response.time }}ms
      </div>
    </div>

    <el-tabs v-model="activeTab" class="response-tabs">
      <!-- 响应体 -->
      <el-tab-pane label="响应体" name="body">
        <div class="response-body">
          <div class="toolbar">
            <el-button-group>
              <el-button :type="viewMode === 'pretty' ? 'primary' : ''" @click="viewMode = 'pretty'">
                格式化
              </el-button>
              <el-button :type="viewMode === 'raw' ? 'primary' : ''" @click="viewMode = 'raw'">
                原始
              </el-button>
            </el-button-group>
            <el-button type="primary" plain icon="CopyDocument" @click="copyResponse">
              复制
            </el-button>
          </div>
          <pre class="response-content" :class="{ 'pretty': viewMode === 'pretty' }">
            {{ formattedResponse }}
          </pre>
        </div>
      </el-tab-pane>

      <!-- 响应头 -->
      <el-tab-pane label="响应头" name="headers">
        <el-table :data="headersList" stripe>
          <el-table-column prop="name" label="名称" width="200" />
          <el-table-column prop="value" label="值" />
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  response: {
    type: Object,
    required: true,
    default: () => ({
      status: null,
      time: 0,
      headers: {},
      data: null
    })
  }
})

const activeTab = ref('body')
const viewMode = ref('pretty')

// 计算属性
const isSuccess = computed(() => {
  return props.response.status >= 200 && props.response.status < 300
})

const headersList = computed(() => {
  return Object.entries(props.response.headers || {}).map(([name, value]) => ({
    name,
    value
  }))
})

const formattedResponse = computed(() => {
  if (!props.response.data) return ''
  
  try {
    if (viewMode.value === 'pretty') {
      return JSON.stringify(props.response.data, null, 2)
    } else {
      return JSON.stringify(props.response.data)
    }
  } catch (e) {
    return String(props.response.data)
  }
})

// 方法
const copyResponse = async () => {
  try {
    await navigator.clipboard.writeText(formattedResponse.value)
    ElMessage.success('已复制到剪贴板')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}
</script>

<style scoped>
.response-viewer {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.status {
  font-size: 16px;
  font-weight: bold;
  color: #f56c6c;
}

.status.success {
  color: #67c23a;
}

.time {
  color: #909399;
}

.response-tabs {
  margin-top: 20px;
}

.toolbar {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}

.response-content {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  overflow: auto;
  font-family: monospace;
  white-space: pre-wrap;
  max-height: 500px;
}

.response-content.pretty {
  line-height: 1.5;
}
</style> 