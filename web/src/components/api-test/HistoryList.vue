<template>
  <div class="history-list">
    <div class="toolbar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索历史记录"
        prefix-icon="Search"
        clearable
      />
      <el-button type="danger" plain @click="clearHistory">
        清空历史
      </el-button>
    </div>

    <el-table
      :data="filteredHistory"
      style="width: 100%"
      :max-height="500"
      @row-click="handleRowClick"
    >
      <el-table-column prop="timestamp" label="时间" width="180">
        <template #default="{ row }">
          {{ formatTime(row.timestamp) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="method" label="方法" width="100">
        <template #default="{ row }">
          <el-tag :type="getMethodType(row.method)">{{ row.method }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="endpoint" label="端点" />
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column fixed="right" label="操作" width="120">
        <template #default="{ row }">
          <el-button link type="primary" @click.stop="replayRequest(row)">
            重放
          </el-button>
          <el-button link type="danger" @click.stop="removeHistoryItem(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const props = defineProps({
  history: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['replay-request', 'remove-item', 'clear-history'])

const searchQuery = ref('')

// 计算属性
const filteredHistory = computed(() => {
  if (!searchQuery.value) return props.history
  
  const query = searchQuery.value.toLowerCase()
  return props.history.filter(item => 
    item.endpoint.toLowerCase().includes(query) ||
    item.method.toLowerCase().includes(query)
  )
})

// 方法
const formatTime = (timestamp) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

const getMethodType = (method) => {
  const types = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger',
    PATCH: 'info'
  }
  return types[method] || ''
}

const getStatusType = (status) => {
  if (status >= 200 && status < 300) return 'success'
  if (status >= 400 && status < 500) return 'warning'
  if (status >= 500) return 'danger'
  return 'info'
}

const handleRowClick = (row) => {
  emit('select-item', row)
}

const replayRequest = (item) => {
  emit('replay-request', item)
}

const removeHistoryItem = async (item) => {
  try {
    await ElMessageBox.confirm('确定要删除这条历史记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    emit('remove-item', item)
    ElMessage.success('已删除历史记录')
  } catch {
    // 用户取消删除
  }
}

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有历史记录吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    emit('clear-history')
    ElMessage.success('已清空历史记录')
  } catch {
    // 用户取消清空
  }
}
</script>

<style scoped>
.history-list {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.toolbar .el-input {
  width: 300px;
}
</style> 