# Image2Video 桌面应用说明

## 概述

Image2Video 桌面应用是一个基于 PyQt6 开发的 GUI 程序，允许用户将图片转换为具有平滑动画和过渡效果的视频。桌面应用与核心库集成，使用 MVC 架构设计。

## 主要功能

- 添加多张图片并批量处理
- 为每张图片添加文字说明
- 自动生成图片对应的语音解说
- 为每张图片设置动画效果（缩放、平移等）
- 设置图片间的转场效果
- 预览单张图片动画效果
- 生成并预览完整视频

## 目录结构

```
desktop/
├── controllers/           # 控制器目录
│   ├── __init__.py
│   ├── audio_controller.py
│   └── video_controller.py
├── models/                # 模型目录 (桥接到核心模型)
│   ├── __init__.py
│   └── image_item.py
├── ui/                    # 用户界面目录
│   ├── __init__.py
│   └── main_window.py
└── main.py                # 程序入口
```

## 架构说明

桌面应用采用 MVC (Model-View-Controller) 架构：

1. **Models**: 通过桥接方式使用核心库的 `ImageItem` 模型
2. **Views**: 基于 PyQt6 实现的 UI 组件
3. **Controllers**: 处理业务逻辑，协调 UI 与核心服务

## 控制器说明

### AudioController
负责管理音频生成和预览相关功能：
- 单个音频生成
- 批量音频生成
- 音频预览

### VideoController
负责管理视频生成和预览相关功能：
- 片段生成
- 完整视频合成
- 应用动画设置
- 视频预览

## 用户界面

主窗口 `MainWindow` 包含以下功能区域：
- 顶部工具栏：添加图片、生成语音、生成视频、预览视频
- 中部内容区：以网格形式展示图片及相关设置
  - 图片预览
  - 文本输入
  - 音频试听
  - 片段生成
  - 动画设置

## 运行方式

可以通过以下方式启动桌面应用：

1. 使用启动脚本：
```bash
# Linux/macOS
./scripts/start_desktop.sh

# Windows
scripts\start_desktop.bat
```

2. 直接通过 Python 运行：
```bash
python -m desktop.main
```

## 依赖项

桌面应用依赖于以下主要库：
- PyQt6：GUI 框架
- core 模块：核心功能库

所有依赖项已在 `requirements.txt` 中列出。

## 扩展和自定义

要添加新功能，可以：
1. 在 `controllers` 目录中创建新的控制器
2. 在 `ui` 目录中添加新的界面组件
3. 修改 `main_window.py` 集成新组件 