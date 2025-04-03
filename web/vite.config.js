import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '^/api/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '^/uploads/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '^/videos/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '^/audio/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    },
    middlewares: [
      (req, res, next) => {
        if (!req.url.match(/^\/(api|uploads|videos|audio|assets)\//)) {
          req.url = '/index.html'
        }
        next()
      }
    ]
  },
  base: '/',
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus']
        }
      }
    }
  }
})
