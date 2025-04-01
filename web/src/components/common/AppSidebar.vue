<template>
  <div class="sidebar-container" :class="{ 'collapsed': sidebarCollapsed }">
    <el-menu
      :collapse="sidebarCollapsed"
      :default-active="activeMenu"
      class="sidebar-menu"
      router
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        <span>首页</span>
      </el-menu-item>
      
      <el-menu-item index="/upload">
        <el-icon><Upload /></el-icon>
        <span>上传管理</span>
      </el-menu-item>
      
      <el-menu-item index="/creator">
        <el-icon><VideoCamera /></el-icon>
        <span>视频创建</span>
      </el-menu-item>
      
      <el-menu-item index="/videos">
        <el-icon><VideoPlay /></el-icon>
        <span>视频管理</span>
      </el-menu-item>
      
      <el-menu-item index="/api-test">
        <el-icon><Connection /></el-icon>
        <span>API测试</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '../../store/modules/app'
import { 
  HomeFilled, 
  Upload, 
  VideoCamera, 
  VideoPlay, 
  Connection 
} from '@element-plus/icons-vue'

const route = useRoute()
const appStore = useAppStore()

// 计算属性：当前激活的菜单项
const activeMenu = computed(() => {
  return route.path
})

// 计算属性：侧边栏是否折叠
const sidebarCollapsed = computed(() => {
  return appStore.sidebarCollapsed
})
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  background-color: #304156;
  transition: width 0.3s;
  width: 210px;
  overflow: hidden;
}

.sidebar-container.collapsed {
  width: 64px;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 210px;
}

/* 重写Element Plus样式 */
:deep(.el-menu-item) {
  height: 56px;
  line-height: 56px;
}

:deep(.el-menu-item.is-active) {
  background-color: #263445 !important;
}

:deep(.el-menu-item:hover) {
  background-color: #263445 !important;
}
</style> 