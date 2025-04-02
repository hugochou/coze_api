# Coze API Web UI API使用指南

本文档详细介绍了Web UI如何与后端API交互，包括所有可用的API端点、参数和调用方式。

## API基础知识

### 基础URL

API基础URL由环境变量`VITE_API_BASE_URL`定义，在开发环境中默认为`http://localhost:8000`。

### 请求格式

- GET请求：用于获取数据
- POST请求：用于创建数据，通常包含JSON格式的请求体
- 文件上传：使用`multipart/form-data`格式

### 响应格式

大多数API响应采用以下JSON格式：

```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

或失败时：

```json
{
  "success": false,
  "error": "错误信息"
}
```

## API端点

### 健康检查

检查API服务是否正常运行。

- **端点**: `/api/health`
- **方法**: GET
- **响应示例**:
  ```json
  {
    "status": "ok",
    "message": "Coze API正常运行",
    "base_url": "http://localhost:8000",
    "environment": "development"
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { getHealthStatus } from '../api';
  
  async function checkHealth() {
    try {
      const result = await getHealthStatus();
      console.log('API状态:', result);
    } catch (error) {
      console.error('健康检查失败:', error);
    }
  }
  ```

### 文件上传

#### 上传图片

上传图片文件到服务器。

- **端点**: `/api/upload/image`
- **方法**: POST
- **请求格式**: `multipart/form-data`
- **参数**:
  - `file`: 图片文件 (支持格式: jpg, jpeg, png, webp, bmp, gif)
- **响应示例**:
  ```json
  {
    "success": true,
    "filename": "image_20240501_123045_abcd1234.jpg",
    "path": "/path/to/uploads/image_20240501_123045_abcd1234.jpg",
    "url": "/uploads/image_20240501_123045_abcd1234.jpg",
    "full_url": "http://localhost:8000/uploads/image_20240501_123045_abcd1234.jpg"
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { uploadImage } from '../api/upload';
  
  async function handleUpload(file) {
    try {
      const result = await uploadImage(file);
      console.log('上传成功:', result);
    } catch (error) {
      console.error('上传失败:', error);
    }
  }
  ```

#### 上传音频

上传音频文件到服务器。

- **端点**: `/api/upload/audio`
- **方法**: POST
- **请求格式**: `multipart/form-data`
- **参数**:
  - `file`: 音频文件 (支持格式: mp3, wav, ogg, m4a)
- **响应示例**:
  ```json
  {
    "success": true,
    "filename": "audio_20240501_123045_abcd1234.mp3",
    "path": "/path/to/uploads/audio_20240501_123045_abcd1234.mp3",
    "url": "/uploads/audio_20240501_123045_abcd1234.mp3",
    "full_url": "http://localhost:8000/uploads/audio_20240501_123045_abcd1234.mp3"
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { uploadAudio } from '../api/upload';
  
  async function handleUpload(file) {
    try {
      const result = await uploadAudio(file);
      console.log('上传成功:', result);
    } catch (error) {
      console.error('上传失败:', error);
    }
  }
  ```

### 音频创建

#### 文本转音频

将文本转换为音频文件。

- **端点**: `/api/audio/create`
- **方法**: POST
- **请求格式**: JSON
- **参数**:
  ```json
  {
    "text": "要转换为音频的文本内容",
    "voice": "zh-cn",  // 可选，语音类型
    "speed": 1.0,      // 可选，语速 (0.5-2.0)
    "format": "mp3"    // 可选，输出格式 (mp3, wav)
  }
  ```
- **响应示例**:
  ```json
  {
    "success": true,
    "filename": "audio_20240501_123045_abcd1234.mp3",
    "path": "/path/to/data/audio/audio_20240501_123045_abcd1234.mp3",
    "url": "/audio/audio_20240501_123045_abcd1234.mp3",
    "full_url": "http://localhost:8000/audio/audio_20240501_123045_abcd1234.mp3"
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { createAudio } from '../api/audio';
  
  async function handleCreateAudio(text, options = {}) {
    try {
      const data = {
        text,
        ...options
      };
      const result = await createAudio(data);
      console.log('音频创建成功:', result);
      return result;
    } catch (error) {
      console.error('音频创建失败:', error);
      throw error;
    }
  }
  ```

### 视频管理

#### 创建视频

基于上传的图片和配置创建视频。

- **端点**: `/api/video/create`
- **方法**: POST
- **请求格式**: JSON
- **参数**:
  ```json
  {
    "images": [
      {
        "id": "1",
        "image_path": "/path/to/image1.jpg",
        "text": "图片描述",
        "audio_path": "/path/to/audio1.mp3",
        "duration": 3,
        "animation": {
          "name": "缩放",
          "scale_from": 1.0,
          "scale_to": 1.2,
          "position_from": [0.5, 0.5],
          "position_to": [0.5, 0.5]
        },
        "order": 0
      },
      {
        "id": "2",
        "image_path": "/path/to/image2.jpg",
        "text": "图片描述",
        "audio_path": null,
        "duration": 3,
        "animation": {
          "name": "缩放平移",
          "scale_from": 1.0,
          "scale_to": 1.2,
          "position_from": [0.4, 0.4],
          "position_to": [0.6, 0.6]
        },
        "order": 1
      }
    ],
    "transition": "淡入淡出",
    "transition_duration": 0.7,
    "output_fps": 30,
    "output_quality": "medium"
  }
  ```
- **响应示例**:
  ```json
  {
    "success": true,
    "video_path": "/path/to/output/video_20240501_123045_abcd1234.mp4",
    "video_url": "/videos/video_20240501_123045_abcd1234.mp4",
    "video_full_url": "http://localhost:8000/videos/video_20240501_123045_abcd1234.mp4",
    "message": "视频创建成功"
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { createVideo } from '../api/video';
  
  async function handleCreateVideo(videoData) {
    try {
      const result = await createVideo(videoData);
      console.log('视频创建成功:', result);
    } catch (error) {
      console.error('视频创建失败:', error);
    }
  }
  ```

#### 获取视频列表

获取所有已创建的视频列表。

- **端点**: `/api/video/list`
- **方法**: GET
- **响应示例**:
  ```json
  {
    "success": true,
    "videos": [
      {
        "filename": "video_20240501_123045_abcd1234.mp4",
        "path": "/path/to/output/video_20240501_123045_abcd1234.mp4",
        "url": "/videos/video_20240501_123045_abcd1234.mp4",
        "full_url": "http://localhost:8000/videos/video_20240501_123045_abcd1234.mp4",
        "size": 1024000,
        "created_at": "2024-05-01 12:30:45"
      },
      {
        "filename": "video_20240430_153012_efgh5678.mp4",
        "path": "/path/to/output/video_20240430_153012_efgh5678.mp4",
        "url": "/videos/video_20240430_153012_efgh5678.mp4",
        "full_url": "http://localhost:8000/videos/video_20240430_153012_efgh5678.mp4",
        "size": 2048000,
        "created_at": "2024-04-30 15:30:12"
      }
    ]
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { getVideoList } from '../api/video';
  
  async function fetchVideos() {
    try {
      const result = await getVideoList();
      const videos = result.videos || [];
      console.log('视频列表:', videos);
    } catch (error) {
      console.error('获取视频列表失败:', error);
    }
  }
  ```

#### 获取视频文件

获取指定的视频文件。

- **端点**: `/api/video/get/<filename>`
- **方法**: GET
- **直接返回视频文件**
- **Web UI调用示例**:
  ```javascript
  import { getVideoUrl } from '../api/video';
  
  function playVideo(filename) {
    const videoUrl = getVideoUrl(filename);
    videoPlayer.src = videoUrl;
    videoPlayer.play();
  }
  ```

### 文件访问

#### 访问上传的文件

- **端点**: `/uploads/<filename>`
- **方法**: GET
- **直接返回文件**

#### 访问视频文件

- **端点**: `/videos/<filename>`
- **方法**: GET
- **直接返回视频文件**

#### 访问音频文件

- **端点**: `/audio/<filename>`
- **方法**: GET
- **直接返回音频文件**

### 文件管理

#### 获取文件列表

获取系统中的文件列表，可按类型筛选。

- **端点**: `/api/file/list`
- **方法**: GET
- **查询参数**:
  - `type`: 文件类型，可选值为 all, image, audio, video
- **响应示例**:
  ```json
  {
    "success": true,
    "files": [
      {
        "name": "file1.jpg",
        "path": "/path/to/file1.jpg",
        "url": "/uploads/file1.jpg",
        "type": "image",
        "size": 1024,
        "modified": "2024-04-01 12:30:45"
      },
      {
        "name": "audio1.mp3",
        "path": "/path/to/audio1.mp3",
        "url": "/audio/audio1.mp3",
        "type": "audio",
        "size": 2048,
        "modified": "2024-04-01 12:35:10"
      }
    ]
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { file } from '../api';
  
  async function fetchFiles(type = 'all') {
    try {
      const result = await file.getFileList(type);
      console.log('文件列表:', result.files);
      return result.files;
    } catch (error) {
      console.error('获取文件列表失败:', error);
    }
  }
  ```

#### 删除文件

删除指定的一个或多个文件。

- **端点**: `/api/file/delete`
- **方法**: POST
- **请求格式**: JSON
- **参数**:
  ```json
  {
    "files": [
      "/path/to/file1.jpg",
      "/path/to/file2.mp3"
    ]
  }
  ```
- **响应示例**:
  ```json
  {
    "success": true,
    "deleted": 2,
    "failed": []
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { file } from '../api';
  
  async function deleteFiles(filePaths) {
    try {
      const result = await file.deleteFiles(filePaths);
      console.log('删除成功:', result.deleted, '个文件');
      if (result.failed.length > 0) {
        console.warn('删除失败:', result.failed.length, '个文件');
      }
      return result;
    } catch (error) {
      console.error('删除文件失败:', error);
    }
  }
  ```

#### 清空文件

清空指定类型的所有文件。

- **端点**: `/api/file/clear`
- **方法**: POST
- **请求格式**: JSON
- **参数**:
  ```json
  {
    "type": "all" // 文件类型，可选值为 all, image, audio, video
  }
  ```
- **响应示例**:
  ```json
  {
    "success": true,
    "message": "成功清空所有文件",
    "cleared": {
      "image": 10,
      "audio": 5,
      "video": 3
    }
  }
  ```
- **Web UI调用示例**:
  ```javascript
  import { file } from '../api';
  
  async function clearFiles(type = 'all') {
    try {
      const result = await file.clearFiles(type);
      console.log('清空文件成功:', result.message);
      return result;
    } catch (error) {
      console.error('清空文件失败:', error);
    }
  }
  ```

## 错误处理

API错误一般通过HTTP状态码和响应体中的错误信息返回：

- 400: 请求错误（例如参数缺失或格式错误）
- 404: 资源不存在
- 500: 服务器内部错误

Web UI中的错误处理示例：

```javascript
try {
  const result = await api.someFunction();
  // 处理成功结果
} catch (error) {
  // 显示错误消息
  const errorMessage = error.response?.data?.error || '未知错误';
  showErrorMessage(errorMessage);
}
```

## API状态管理

Web UI使用Pinia进行API状态管理，主要包含以下Store：

- `appStore`: 管理应用全局状态和API连接状态
- `uploadStore`: 管理上传文件的状态
- `videoStore`: 管理视频创建和列表状态

使用示例：

```javascript
import { useAppStore } from '../store/modules/app';
import { useUploadStore } from '../store/modules/upload';
import { useVideoStore } from '../store/modules/video';

// 在组件中使用
const appStore = useAppStore();
const uploadStore = useUploadStore();
const videoStore = useVideoStore();

// 检查API状态
await appStore.checkApiHealth();

// 上传图片
await uploadStore.uploadImage(file);

// 创建视频
await videoStore.createVideo();
```

## API测试工具

Web UI提供了API测试工具，可用于直接测试各个API端点：

1. 在导航菜单中选择"API测试"
2. 选择要测试的API端点
3. 设置必要的参数
4. 点击"发送请求"按钮
5. 查看响应结果

## 附录：支持的动画类型

视频创建时支持以下动画效果：

- `缩放`: 简单缩放效果
- `平移`: 简单平移效果
- `缩放平移`: 组合缩放和平移效果
- `旋转`: 旋转效果
- `淡入淡出`: 透明度变化效果

## 附录：支持的转场效果

视频创建时支持以下转场效果：

- `淡入淡出`: 透明度过渡
- `滑动`: 滑动过渡
- `缩放`: 缩放过渡
- `旋转`: 旋转过渡 