# Image2Video API 接口文档

本文档详细说明了 Image2Video API 服务的所有接口，包括请求参数、响应格式和示例代码。

## 基本信息

- **基础URL**: `http://localhost:8000`
- **请求格式**: JSON
- **响应格式**: JSON

## 健康检查

用于检查API服务是否正常运行。

- **URL**: `/api/health`
- **方法**: `GET`
- **鉴权**: 无

### 响应

```json
{
  "status": "ok",
  "message": "Image2Video API正常运行"
}
```

## 文件上传接口

### 上传图片

上传一张图片文件。

- **URL**: `/api/upload/image`
- **方法**: `POST`
- **Content-Type**: `multipart/form-data`
- **鉴权**: 无

### 请求参数

| 字段名 | 必填 | 类型 | 描述 |
|-------|------|------|------|
| file  | 是   | File | 图片文件 |

### 响应

```json
{
  "success": true,
  "filename": "image_20231224_123045_a1b2c3d4.jpg",
  "path": "/path/to/uploads/image_20231224_123045_a1b2c3d4.jpg",
  "url": "/uploads/image_20231224_123045_a1b2c3d4.jpg"
}
```

### 错误响应

```json
{
  "success": false,
  "error": "没有文件"
}
```

### 示例代码

```python
import requests

url = "http://localhost:8000/api/upload/image"
files = {'file': open('path/to/image.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### 上传音频

上传一个音频文件。

- **URL**: `/api/upload/audio`
- **方法**: `POST`
- **Content-Type**: `multipart/form-data`
- **鉴权**: 无

### 请求参数

| 字段名 | 必填 | 类型 | 描述 |
|-------|------|------|------|
| file  | 是   | File | 音频文件 |

### 响应

```json
{
  "success": true,
  "filename": "audio_20231224_123045_a1b2c3d4.mp3",
  "path": "/path/to/uploads/audio_20231224_123045_a1b2c3d4.mp3",
  "url": "/uploads/audio_20231224_123045_a1b2c3d4.mp3"
}
```

### 错误响应

```json
{
  "success": false,
  "error": "不支持的音频格式"
}
```

### 示例代码

```python
import requests

url = "http://localhost:8000/api/upload/audio"
files = {'file': open('path/to/audio.mp3', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

## 视频处理接口

### 创建视频

从上传的图片创建视频。

- **URL**: `/api/video/create`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **鉴权**: 无

### 请求参数

| 字段名 | 必填 | 类型 | 描述 |
|-------|------|------|------|
| images | 是 | Array | 图片项数组，每项包含 id, image_path, duration, animation 等 |
| transition | 否 | String | 转场效果名称，默认为 "淡入淡出" |
| transition_duration | 否 | Number | 转场持续时间，默认为 0.7 |
| output_fps | 否 | Number | 输出视频帧率，默认为 30 |
| output_quality | 否 | String | 输出视频质量，可选值: "low", "medium", "high"，默认为 "medium" |

### 请求体示例

```json
{
  "images": [
    {
      "id": "1",
      "image_path": "/path/to/uploads/image1.jpg",
      "duration": 5,
      "animation": "放大"
    },
    {
      "id": "2",
      "image_path": "/path/to/uploads/image2.jpg",
      "duration": 4,
      "animation": "缩小",
      "audio_path": "/path/to/uploads/audio2.mp3"
    }
  ],
  "transition": "淡入淡出",
  "transition_duration": 0.7,
  "output_fps": 30,
  "output_quality": "high"
}
```

### 响应

```json
{
  "success": true,
  "video_path": "/path/to/output/video_20231224_123045_a1b2c3d4.mp4",
  "video_url": "/videos/video_20231224_123045_a1b2c3d4.mp4",
  "message": "视频创建成功"
}
```

### 错误响应

```json
{
  "success": false,
  "error": "未提供图片数据"
}
```

### 示例代码

```python
import requests
import json

url = "http://localhost:8000/api/video/create"
headers = {'Content-Type': 'application/json'}
data = {
  "images": [
    {
      "id": "1",
      "image_path": "/path/to/uploads/image1.jpg",
      "duration": 5,
      "animation": "放大"
    },
    {
      "id": "2",
      "image_path": "/path/to/uploads/image2.jpg",
      "duration": 4,
      "animation": "缩小"
    }
  ],
  "transition": "淡入淡出",
  "output_quality": "high"
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

### 获取视频列表

获取所有已生成的视频列表。

- **URL**: `/api/video/list`
- **方法**: `GET`
- **鉴权**: 无

### 响应

```json
{
  "success": true,
  "videos": [
    {
      "filename": "video_20231224_123045_a1b2c3d4.mp4",
      "path": "/path/to/output/video_20231224_123045_a1b2c3d4.mp4",
      "url": "/videos/video_20231224_123045_a1b2c3d4.mp4",
      "size": 12345678,
      "created_at": "2023-12-24 12:30:45"
    },
    {
      "filename": "video_20231223_183012_e5f6g7h8.mp4",
      "path": "/path/to/output/video_20231223_183012_e5f6g7h8.mp4",
      "url": "/videos/video_20231223_183012_e5f6g7h8.mp4",
      "size": 8765432,
      "created_at": "2023-12-23 18:30:12"
    }
  ]
}
```

### 示例代码

```python
import requests

url = "http://localhost:8000/api/video/list"
response = requests.get(url)
print(response.json())
```

### 获取视频文件

获取已生成的视频文件。

- **URL**: `/api/video/get/<filename>`
- **方法**: `GET`
- **鉴权**: 无

### 路径参数

| 字段名 | 必填 | 类型 | 描述 |
|-------|------|------|------|
| filename | 是 | String | 视频文件名 |

### 响应

返回视频文件内容，Content-Type 为 `video/mp4`。

### 错误响应

```json
{
  "success": false,
  "error": "视频文件不存在"
}
```

### 示例代码

```python
import requests

filename = "video_20231224_123045_a1b2c3d4.mp4"
url = f"http://localhost:8000/api/video/get/{filename}"

response = requests.get(url)
if response.headers['Content-Type'] == 'video/mp4':
    with open(f"downloaded_{filename}", 'wb') as f:
        f.write(response.content)
else:
    print(response.json())
```

## 静态文件访问

### 访问上传的文件

- **URL**: `/uploads/<filename>`
- **方法**: `GET`
- **鉴权**: 无

### 访问生成的视频

- **URL**: `/videos/<filename>`
- **方法**: `GET`
- **鉴权**: 无

## 常见错误状态码

| 状态码 | 描述 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 动画效果列表

可用于 `animation` 字段的值：

| 名称 | 描述 |
|-----|-----|
| 无 | 无动画效果 |
| 放大 | 图片从原始尺寸向外放大 |
| 缩小 | 图片从放大状态缩小到原始尺寸 |
| 轻微放大 | 图片轻微放大 |
| 轻微缩小 | 图片轻微缩小 |
| 左到右 | 图片从左向右移动 |
| 右到左 | 图片从右向左移动 |
| 上到下 | 图片从上向下移动 |
| 下到上 | 图片从下向上移动 |
| 左上到右下 | 图片从左上向右下移动 |
| 右上到左下 | 图片从右上向左下移动 |
| 随机 | 随机选择一种动画效果 |

## 转场效果列表

可用于 `transition` 字段的值：

| 名称 | 描述 |
|-----|-----|
| 无 | 无转场效果 |
| 淡入淡出 | 场景间平滑交叉溶解 |
| 滑动-左 | 新场景从左侧滑入 |
| 滑动-右 | 新场景从右侧滑入 |
| 滑动-上 | 新场景从顶部滑入 |
| 滑动-下 | 新场景从底部滑入 |
| 缩放淡入 | 新场景逐渐放大进入 |
| 旋转淡入 | 新场景旋转进入 |
| 百叶窗 | 像百叶窗一样逐渐显示新场景 |
| 闪白过渡 | 通过闪白效果过渡到新场景 |
| 随机 | 随机选择一种转场效果 | 