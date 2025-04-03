<template>
  <div class="not-found">
    <div class="content">
      <el-result
        icon="error"
        title="404"
        sub-title="抱歉，您访问的页面不存在"
      >
        <template #extra>
          <el-button type="primary" @click="goHome">返回首页</el-button>
          <el-button @click="goBack">返回上一页</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.not-found {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.content {
  background-color: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

:deep(.el-result__icon) {
  width: 120px;
  height: 120px;
}

:deep(.el-result__title) {
  font-size: 48px;
  color: #303133;
  margin-top: 20px;
}

:deep(.el-result__sub-title) {
  font-size: 20px;
  color: #606266;
  margin-top: 10px;
}

:deep(.el-result__extra) {
  margin-top: 30px;
}
</style> 