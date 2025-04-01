<template>
  <div class="app-container">
    <app-header />
    <div class="main-container">
      <app-sidebar />
      <div class="content-container">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from './store/modules/app'
import AppHeader from './components/common/AppHeader.vue'
import AppSidebar from './components/common/AppSidebar.vue'

const appStore = useAppStore()

// 组件加载时检查API服务健康状态
onMounted(async () => {
  try {
    await appStore.checkApiHealth()
  } catch (error) {
    console.error('API服务检查失败:', error)
  }
})
</script>

<style scoped>
.app-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.main-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.content-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
