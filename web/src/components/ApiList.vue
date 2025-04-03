<template>
  <div class="api-list">
    <el-collapse v-model="activeNames">
      <!-- 视频相关API -->
      <el-collapse-item title="视频相关API" name="video">
        <div class="api-group">
          <div v-for="api in videoApis" :key="api.path" class="api-item">
            <div class="api-name">{{ api.name }}</div>
            <div class="api-actions">
              <el-button
                type="primary"
                link
                :icon="InfoFilled"
                @click.stop="showApiInfo(api)"
              />
              <el-button
                type="primary"
                link
                :icon="Position"
                @click.stop="selectApi(api)"
              />
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 上传相关API -->
      <el-collapse-item title="上传相关API" name="upload">
        <div class="api-group">
          <div v-for="api in uploadApis" :key="api.path" class="api-item">
            <div class="api-name">{{ api.name }}</div>
            <div class="api-actions">
              <el-button
                type="primary"
                link
                :icon="InfoFilled"
                @click.stop="showApiInfo(api)"
              />
              <el-button
                type="primary"
                link
                :icon="Position"
                @click.stop="selectApi(api)"
              />
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 音频相关API -->
      <el-collapse-item title="音频相关API" name="audio">
        <div class="api-group">
          <div v-for="api in audioApis" :key="api.path" class="api-item">
            <div class="api-name">{{ api.name }}</div>
            <div class="api-actions">
              <el-button
                type="primary"
                link
                :icon="InfoFilled"
                @click.stop="showApiInfo(api)"
              />
              <el-button
                type="primary"
                link
                :icon="Position"
                @click.stop="selectApi(api)"
              />
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 文件管理API -->
      <el-collapse-item title="文件管理API" name="file">
        <div class="api-group">
          <div v-for="api in fileApis" :key="api.path" class="api-item">
            <div class="api-name">{{ api.name }}</div>
            <div class="api-actions">
              <el-button
                type="primary"
                link
                :icon="InfoFilled"
                @click.stop="showApiInfo(api)"
              />
              <el-button
                type="primary"
                link
                :icon="Position"
                @click.stop="selectApi(api)"
              />
            </div>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>

    <!-- API详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentApi?.name"
      width="50%"
      class="api-info-dialog"
    >
      <div class="api-info" v-if="currentApi">
        <div class="info-section">
          <h3>基本信息</h3>
          <div class="info-item">
            <span class="label">请求方式：</span>
            <el-tag :type="getMethodType(currentApi.method)">{{ currentApi.method }}</el-tag>
          </div>
          <div class="info-item">
            <span class="label">接口地址：</span>
            <code>{{ currentApi.path }}</code>
          </div>
          <div class="info-item">
            <span class="label">接口描述：</span>
            <span>{{ currentApi.description }}</span>
          </div>
        </div>

        <div class="info-section" v-if="currentApi.params">
          <h3>参数说明</h3>
          <div v-if="currentApi.params.query">
            <h4>Query参数</h4>
            <el-table :data="formatParams(currentApi.params.query)" border>
              <el-table-column prop="name" label="参数名" width="180" />
              <el-table-column prop="type" label="类型" width="180" />
              <el-table-column prop="required" label="是否必须" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.required ? 'danger' : 'info'">
                    {{ scope.row.required ? '是' : '否' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="说明" />
            </el-table>
          </div>
          
          <div v-if="currentApi.params.body">
            <h4>请求体参数</h4>
            <el-table :data="formatParams(currentApi.params.body)" border>
              <el-table-column prop="name" label="参数名" width="180" />
              <el-table-column prop="type" label="类型" width="180" />
              <el-table-column prop="required" label="是否必须" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.required ? 'danger' : 'info'">
                    {{ scope.row.required ? '是' : '否' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="说明" />
            </el-table>
          </div>
        </div>

        <div class="info-section" v-if="currentApi.example">
          <h3>使用示例</h3>
          <div class="example-section">
            <h4>请求示例</h4>
            <pre><code>{{ JSON.stringify(currentApi.example.request, null, 2) }}</code></pre>
          </div>
          <div class="example-section">
            <h4>响应示例</h4>
            <pre><code>{{ JSON.stringify(currentApi.example.response, null, 2) }}</code></pre>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleUseApi">
            使用此API
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { InfoFilled, Position } from '@element-plus/icons-vue'

const activeNames = ref(['video'])
const dialogVisible = ref(false)
const currentApi = ref(null)

const videoApis = [
  {
    name: '创建视频',
    method: 'POST',
    path: '/api/video/create',
    description: '创建一个新的视频，支持设置动画效果、转场效果和音频',
    params: {
      body: {
        images: {
          type: 'Array<Object>',
          required: true,
          description: '图片列表，每个图片对象包含路径、动画效果等'
        },
        transition: {
          type: 'string',
          required: false,
          description: '转场效果类型，选项：["无", "淡入淡出", "滑动-左", "滑动-右", "滑动-上", "滑动-下", "缩放淡入", "旋转淡入", "百叶窗", "扭曲溶解", "闪白过渡", "随机"]'
        },
        transition_duration: {
          type: 'number',
          required: false,
          description: '转场效果持续时间（秒）'
        },
        output_fps: {
          type: 'number',
          required: false,
          description: '输出视频的帧率'
        },
        output_quality: {
          type: 'string',
          required: false,
          description: '输出视频质量（high/medium/low）'
        }
      }
    },
    example: {
      request: {
        images: [
          {
            path: '/uploads/image1.jpg',
            duration: 3,
            animation: 'zoom-in'
          }
        ],
        transition: 'fade',
        transition_duration: 1,
        output_fps: 30,
        output_quality: 'high'
      },
      response: {
        status: 'success',
        data: {
          video_id: '12345',
          output_path: '/videos/output.mp4'
        }
      }
    }
  },
  {
    name: '单图音频视频创建',
    method: 'POST',
    path: '/api/video/image2video',
    description: '从单张图片和音频创建视频，支持自定义动画效果',
    params: {
      body: {
        image_path: {
          type: 'string',
          required: true,
          description: '图片文件路径'
        },
        audio_path: {
          type: 'string',
          required: true,
          description: '音频文件路径'
        },
        animation_scale: {
          type: 'string',
          required: false,
          description: '缩放动画类型，选项：["无", "放大", "缩小", "轻微放大", "轻微缩小", "剧烈放大", "脉动", "随机"]'
        },
        animation_position: {
          type: 'string',
          required: false,
          description: '平移动画类型，选项：["无", "左到右", "右到左", "上到下", "下到上", "左上到右下", "右上到左下", "左下到右上", "右下到左上", "轻微左右", "轻微上下", "随机"]'
        },
        animation_curve: {
          type: 'string',
          required: false,
          description: '动画曲线类型，选项：["线性", "缓入", "缓出", "缓入缓出", "强缓入", "强缓出", "平滑弹入", "平滑弹出", "随机"]'
        },
        output_fps: {
          type: 'number',
          required: false,
          description: '输出视频的帧率'
        },
        output_quality: {
          type: 'string',
          required: false,
          description: '输出视频质量（high/medium/low）'
        }
      }
    },
    example: {
      request: {
        image_path: '/uploads/image1.jpg',
        audio_path: '/uploads/audio1.mp3',
        animation_scale: '放大',
        animation_position: '左到右',
        animation_curve: '缓入缓出',
        output_fps: 30,
        output_quality: 'high'
      },
      response: {
        success: true,
        video_path: '/path/to/video.mp4',
        video_url: '/videos/video.mp4',
        video_full_url: 'http://localhost:8000/videos/video.mp4'
      }
    }
  },
  {
    name: '视频合并',
    method: 'POST',
    path: '/api/video/videos2video',
    description: '将多段视频合并成一个视频，支持转场效果',
    params: {
      body: {
        video_paths: {
          type: 'Array<string>',
          required: true,
          description: '视频文件路径列表'
        },
        transition: {
          type: 'string',
          required: false,
          description: '转场效果类型，选项：["无", "淡入淡出", "滑动-左", "滑动-右", "滑动-上", "滑动-下", "缩放淡入", "旋转淡入", "百叶窗", "扭曲溶解", "闪白过渡", "随机"]'
        },
        transition_duration: {
          type: 'number',
          required: false,
          description: '转场效果持续时间（秒）'
        },
        output_fps: {
          type: 'number',
          required: false,
          description: '输出视频的帧率，默认使用第一个视频的帧率'
        },
        output_quality: {
          type: 'string',
          required: false,
          description: '输出视频质量（high/medium/low）'
        }
      }
    },
    example: {
      request: {
        video_paths: [
          '/videos/video1.mp4',
          '/videos/video2.mp4'
        ],
        transition: '淡入淡出',
        transition_duration: 0.7,
        output_quality: 'high'
      },
      response: {
        success: true,
        video_path: '/path/to/combined.mp4',
        video_url: '/videos/combined.mp4',
        video_full_url: 'http://localhost:8000/videos/combined.mp4'
      }
    }
  },
  {
    name: '获取视频列表',
    method: 'GET',
    path: '/api/video/list',
    description: '获取所有已生成的视频列表'
  },
  {
    name: '获取视频文件',
    method: 'GET',
    path: '/api/video/get/:filename',
    description: '获取指定的视频文件',
    params: {
      query: {
        filename: {
          type: 'string',
          required: true,
          description: '视频文件名'
        }
      }
    }
  }
]

const uploadApis = [
  {
    name: '上传图片',
    method: 'POST',
    path: '/api/upload/image',
    description: '上传图片文件',
    params: {
      body: {
        file: {
          type: 'File',
          required: true,
          description: '要上传的图片文件'
        }
      }
    }
  },
  {
    name: '上传音频',
    method: 'POST',
    path: '/api/upload/audio',
    description: '上传音频文件',
    params: {
      body: {
        file: {
          type: 'File',
          required: true,
          description: '要上传的音频文件'
        }
      }
    }
  }
]

const audioApis = [
  {
    name: '创建音频',
    method: 'POST',
    path: '/api/audio/create',
    description: '通过文本创建音频文件',
    params: {
      body: {
        text: {
          type: 'string',
          required: true,
          description: '要转换的文本内容'
        },
        voice: {
          type: 'string',
          required: false,
          description: '语音类型'
        },
        speed: {
          type: 'number',
          required: false,
          description: '语速（0.5-2.0）'
        },
        format: {
          type: 'string',
          required: false,
          description: '输出格式（mp3/wav）'
        }
      }
    }
  }
]

const fileApis = [
  {
    name: '获取文件列表',
    method: 'GET',
    path: '/api/file/list',
    description: '获取指定类型的文件列表',
    params: {
      query: {
        type: {
          type: 'string',
          required: false,
          description: '文件类型（image/audio/video）'
        }
      }
    }
  },
  {
    name: '删除文件',
    method: 'POST',
    path: '/api/file/delete',
    description: '删除指定的文件',
    params: {
      body: {
        files: {
          type: 'Array<string>',
          required: true,
          description: '要删除的文件路径列表'
        }
      }
    }
  },
  {
    name: '清空文件',
    method: 'POST',
    path: '/api/file/clear',
    description: '清空指定类型的所有文件',
    params: {
      body: {
        type: {
          type: 'string',
          required: true,
          description: '文件类型（image/audio/video）'
        }
      }
    }
  }
]

// 显示API详情
const showApiInfo = (api) => {
  currentApi.value = api
  dialogVisible.value = true
}

// 选择API
const selectApi = (api) => {
  emit('select', api)
}

// 在弹窗中使用API
const handleUseApi = () => {
  selectApi(currentApi.value)
  dialogVisible.value = false
}

// 获取请求方法对应的类型
const getMethodType = (method) => {
  const types = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger'
  }
  return types[method] || 'info'
}

// 格式化参数为表格数据
const formatParams = (params) => {
  return Object.entries(params).map(([name, param]) => ({
    name,
    type: param.type || param,
    required: param.required !== undefined ? param.required : !param.includes('?'),
    description: param.description || '-'
  }))
}

const emit = defineEmits(['select'])
</script>

<style scoped>
.api-list {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin: 10px 0;
}

.api-group {
  padding: 10px;
}

.api-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  margin: 4px 0;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.api-item:hover {
  background-color: #f5f7fa;
}

.api-name {
  font-size: 14px;
  color: #303133;
}

.api-actions {
  display: flex;
  gap: 8px;
}

.info-section {
  margin-bottom: 20px;
}

.info-section h3 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.info-section h4 {
  font-size: 14px;
  margin: 12px 0;
}

.info-item {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.info-item .label {
  width: 100px;
  color: #606266;
}

.example-section {
  margin-bottom: 16px;
}

.example-section pre {
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  margin: 8px 0;
  overflow-x: auto;
}

:deep(.el-collapse-item__header) {
  padding-left: 15px;
  font-weight: bold;
}

:deep(.api-info-dialog .el-dialog__body) {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}
</style> 