# Image2Video 部署指南

本文档提供了 Image2Video 项目的完整部署指南，包括环境配置、安装步骤和启动方法。

## 环境要求

- Python 3.8+ 
- FFmpeg (用于视频处理)
- 足够的磁盘空间用于存储媒体文件

## 系统依赖

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg
```

### CentOS/RHEL

```bash
sudo yum update
sudo yum install -y python3 python3-pip ffmpeg
```

### macOS

```bash
brew update
brew install python ffmpeg
```

## 项目安装

1. 克隆代码仓库

```bash
git clone https://github.com/yourusername/image2video.git
cd image2video
```

2. 创建并激活虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

## API服务部署

### 开发环境运行

使用提供的脚本启动API服务:

```bash
chmod +x scripts/start_api.sh
./scripts/start_api.sh
```

默认情况下，API服务将在 `http://0.0.0.0:8000` 上运行。

### 使用 Gunicorn 部署

对于生产环境，建议使用 Gunicorn 做为 WSGI 服务器:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "api.app:create_app()"
```

### 使用 Systemd 设置开机启动 (Linux)

1. 创建 systemd 服务文件:

```bash
sudo nano /etc/systemd/system/image2video-api.service
```

2. 添加以下内容:

```
[Unit]
Description=Image2Video API Service
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/image2video
Environment="PATH=/path/to/image2video/venv/bin"
ExecStart=/path/to/image2video/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 "api.app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

3. 启用并启动服务:

```bash
sudo systemctl daemon-reload
sudo systemctl enable image2video-api
sudo systemctl start image2video-api
```

### 使用 Nginx 反向代理

对于生产环境，建议使用 Nginx 作为反向代理:

1. 安装 Nginx:

```bash
sudo apt install nginx  # Debian/Ubuntu
sudo yum install nginx  # CentOS/RHEL
```

2. 创建 Nginx 配置文件:

```bash
sudo nano /etc/nginx/sites-available/image2video
```

3. 添加以下内容:

```
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        alias /path/to/image2video/data/uploads/;
    }

    location /videos/ {
        alias /path/to/image2video/data/output/;
    }
}
```

4. 启用配置并重启 Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/image2video /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 桌面应用部署

### 运行桌面应用

使用提供的脚本启动桌面应用:

```bash
chmod +x scripts/start_desktop.sh
./scripts/start_desktop.sh
```

### 创建桌面快捷方式 (Linux)

1. 创建 `.desktop` 文件:

```bash
nano ~/.local/share/applications/image2video.desktop
```

2. 添加以下内容:

```
[Desktop Entry]
Name=Image2Video
Comment=图片转视频工具
Exec=/path/to/image2video/scripts/start_desktop.sh
Icon=/path/to/image2video/config/icon.png
Terminal=false
Type=Application
Categories=Utility;
```

## 环境变量配置

可以通过环境变量控制应用行为:

- `API_HOST`: API服务主机地址，默认为 "0.0.0.0"
- `API_PORT`: API服务端口，默认为 8000
- `API_DEBUG`: 是否开启调试模式，设为 "1" 开启
- `LOG_LEVEL`: 日志级别，可选 "DEBUG", "INFO", "WARNING", "ERROR"

### 示例:

```bash
export API_PORT=9000
export LOG_LEVEL=DEBUG
./scripts/start_api.sh
```

## 故障排除

### 常见问题:

1. **导入错误**: 确保你的环境中安装了所有依赖

```bash
pip install -r requirements.txt
```

2. **FFmpeg 错误**: 确保 FFmpeg 已正确安装且在系统路径中

```bash
ffmpeg -version
```

3. **权限问题**: 确保应用有权限写入数据目录

```bash
chmod -R 755 data/
```

4. **端口占用**: 如果端口被占用，可以使用不同的端口

```bash
./scripts/start_api.sh --port=8080
``` 