# Coze API Web UI 部署指南

本文档提供了 Coze API Web UI 部署的最佳实践和注意事项，特别是关于如何处理前端和后端API服务的域名和端口配置。

## 环境配置管理

Web UI 使用环境变量来管理不同环境下的配置，包括API服务的地址。

### 环境变量文件

项目中包含以下环境变量文件：

- `.env`: 所有环境的默认值
- `.env.development`: 开发环境的配置
- `.env.production`: 生产环境的配置

这些文件中主要配置了 `VITE_API_BASE_URL` 变量，用于指定API服务的基础URL。

## API服务地址配置的最佳实践

在真实部署环境中，处理API服务地址配置的最佳实践如下：

### 1. 相对路径方式（推荐）

如果前端和API服务部署在同一个域名下（例如通过反向代理），可以使用相对路径：

```
# API基础URL（相对路径）
VITE_API_BASE_URL=
```

这样前端会请求同一域名下的API路径，无需关心具体的域名和端口。

配置示例（`.env.production`）：
```
VITE_API_BASE_URL=
```

这种方式要求在Web服务器（如Nginx）中正确配置代理，例如：

```nginx
server {
    listen 80;
    server_name example.com;

    # 前端静态文件
    location / {
        root /path/to/web/dist;
        try_files $uri $uri/ /index.html;
    }

    # API服务代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 上传文件访问
    location /uploads/ {
        proxy_pass http://localhost:8000;
    }

    # 视频文件访问
    location /videos/ {
        proxy_pass http://localhost:8000;
    }
}
```

### 2. 绝对URL方式

如果前端和API服务部署在不同域名或无法使用相对路径，则使用完整的URL：

配置示例（`.env.production`）：
```
VITE_API_BASE_URL=https://api.example.com
```

这种方式需要确保API服务正确配置了CORS（跨域资源共享）：

```python
# 在Flask应用中配置CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://web.example.com"}})
```

### 3. 运行时配置（高级）

对于需要在不同环境灵活切换API地址的情况，可以实现运行时配置：

1. 创建配置文件（在构建后可修改）：

```javascript
// 放在 public/config.js
window.APP_CONFIG = {
  API_BASE_URL: 'https://api.example.com'
};
```

2. 在 `index.html` 中引入：

```html
<script src="/config.js"></script>
```

3. 在API请求中使用：

```javascript
const apiBaseUrl = window.APP_CONFIG?.API_BASE_URL || import.meta.env.VITE_API_BASE_URL;
```

## 部署步骤

### 前端构建

1. 设置生产环境API地址：

```bash
# 设置相对路径（与后端同域部署）
echo "VITE_API_BASE_URL=" > .env.production

# 或设置绝对URL（不同域部署）
echo "VITE_API_BASE_URL=https://api.example.com" > .env.production
```

2. 构建前端项目：

```bash
npm run build
```

3. 将 `dist` 目录部署到Web服务器。

### 后端配置

1. 确保后端API服务正确配置了所有必要的头部和CORS（如果需要）：

```python
# 配置CORS处理
app.config['CORS_HEADERS'] = 'Content-Type,Authorization'
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 确保正确设置了BASE_URL
app.config['API_BASE_URL'] = 'https://api.example.com'  # 或动态获取
```

2. 如果使用相对路径方案，确保后端服务的上下文路径正确。

## 注意事项

1. **安全考虑**：
   - 在生产环境中，总是使用HTTPS
   - 限制CORS的origins不要使用"*"，而是指定允许的域名

2. **URL路径**：
   - 确保API路径、上传文件路径和视频路径在部署环境中一致
   - 如有必要，调整vite.config.js中的代理规则以匹配实际路径

3. **环境变量命名**：
   - 确保所有以`VITE_`开头的环境变量都会暴露给前端代码
   - 敏感信息不应使用`VITE_`前缀

4. **部署检查清单**：
   - ✓ 配置了正确的API地址
   - ✓ 设置了适当的CORS配置
   - ✓ 静态资源路径正确
   - ✓ 文件上传和视频播放路径正确
   - ✓ 服务器反向代理配置正确（如果适用）

## 故障排除

如果部署后遇到API连接问题：

1. 检查浏览器控制台中是否有CORS错误
2. 验证API服务是否正常运行（使用健康检查端点）
3. 确认环境变量是否正确加载
4. 检查网络请求URL是否正确（使用浏览器网络工具）
5. 验证反向代理配置是否正确
6. 检查API服务的日志寻找错误信息 