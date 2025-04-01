<template>
  <div class="api-test-container">
    <h2 class="page-title">API测试</h2>
    <el-result
      icon="info"
      title="功能开发中"
      sub-title="API测试功能正在开发中，敬请期待..."
    >
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
// API测试页面的具体实现将在后续开发
</script>

<style scoped>
.api-test-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}
</style> 