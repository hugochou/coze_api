# Coze API

一个强大的工具，可以将多张图片转换成视频，支持动画效果、转场和音频。

## 项目特点

- 支持多种动画效果（缩放、平移等）
- 支持多种转场效果（淡入淡出、滑动等）
- 支持为每张图片添加音频
- 提供Web API接口
- 提供桌面应用界面
- 高质量视频输出

## 项目结构

```
coze_api/
│
├── api/                   # Web API
│   ├── routes/            # API路由
│   └── app.py             # API主入口
│
├── core/                  # 核心功能模块
│   ├── models/            # 数据模型
│   ├── services/          # 服务层
│   └── utils/             # 工具函数
│
├── desktop/               # 桌面应用
│   ├── controllers/       # 控制器
│   ├── ui/                # 用户界面
│   └── main.py            # 桌面应用主入口
│
├── data/                  # 数据目录
│   ├── uploads/           # 上传的文件
│   ├── output/            # 生成的视频
│   └── temp/              # 临时文件
│
├── config/                # 配置文件
├── docs/                  # 文档
├── scripts/               # 脚本
└── tests/                 # 测试
```

## 安装与运行

### 环境要求

- Python 3.8+
- FFmpeg

### 安装

1. 克隆代码库

```bash
git clone https://github.com/yourusername/coze_api.git
cd coze_api
```

2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 运行API服务

```bash
./scripts/start_api.sh
# 或者指定端口
./scripts/start_api.sh --port=8080
# 开启调试模式
./scripts/start_api.sh --debug
```

### 运行桌面应用

```bash
./scripts/start_desktop.sh
```

## API文档

### 健康检查

```
GET /api/health
```

### 上传图片

```
POST /api/upload/image
```

### 上传音频

```
POST /api/upload/audio
```

### 创建视频

```
POST /api/video/create
```

### 获取视频列表

```
GET /api/video/list
```

### 获取视频文件

```
GET /api/video/get/<filename>
```

## 许可证

[MIT](LICENSE) 