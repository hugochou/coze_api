<template>
  <div class="creator-container">
    <h2 class="page-title">视频创建</h2>
    <el-result
      icon="info"
      title="功能开发中"
      sub-title="视频创建功能正在开发中，敬请期待..."
    >
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
// 视频创建页面的具体实现将在后续开发
</script>

<style scoped>
.creator-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}
</style> 