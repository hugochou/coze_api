import os
import sys
import uuid
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any, Union
from datetime import datetime
import argparse
import traceback

# 将项目根目录添加到Python路径，确保能够导入core模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify, send_file, abort, send_from_directory
from flask_cors import CORS

from config import settings
from core.utils.path_utils import PathUtils
from core.services.animation_service import AnimationService
from core.services.transition_service import TransitionService
from api.routes import register_blueprints

# 配置日志
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("image2video-api")

def create_app():
    """创建并配置Flask应用"""
    # 创建Flask应用
    app = Flask(__name__)
    
    # 配置CORS以允许跨域请求
    CORS(app)
    
    # 注册所有路由蓝图
    register_blueprints(app)
    
    # 配置静态文件访问
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        """提供上传的文件"""
        path_utils = PathUtils()
        uploads_dir = path_utils.get_uploads_dir()
        return send_from_directory(uploads_dir, filename)
    
    @app.route('/videos/<path:filename>')
    def serve_video(filename):
        """提供生成的视频文件"""
        path_utils = PathUtils()
        output_dir = path_utils.get_output_dir()
        return send_from_directory(output_dir, filename)
    
    # 添加健康检查路由
    @app.route('/api/health')
    def health_check():
        """API健康检查"""
        return jsonify({
            "status": "ok",
            "message": "Image2Video API正常运行",
            "base_url": settings.API_BASE_URL,
            "environment": os.environ.get("FLASK_ENV", "development")
        })
    
    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "找不到请求的资源"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "服务器内部错误"}), 500
    
    # 记录所有请求
    @app.before_request
    def log_request_info():
        app.logger.info(f"请求: {request.method} {request.path}")
    
    return app

def main():
    """主入口函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='启动Image2Video API服务')
    parser.add_argument('--port', type=int, default=settings.API_PORT, help='服务端口号')
    parser.add_argument('--host', type=str, default=settings.API_HOST, help='服务主机地址')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args = parser.parse_args()
    
    # 创建应用
    app = create_app()
    
    # 确保所需目录存在
    path_utils = PathUtils()
    path_utils.get_uploads_dir()
    path_utils.get_output_dir()
    path_utils.get_temp_dir()
    
    # 更新环境变量中的API_BASE_URL
    if settings.API_HOST != args.host or settings.API_PORT != args.port:
        os.environ["API_BASE_URL"] = f"http://{args.host}:{args.port}"
        logger.info(f"更新API_BASE_URL为: {os.environ['API_BASE_URL']}")
    
    # 输出服务信息
    logger.info(f"启动Image2Video API服务 @ http://{args.host}:{args.port}")
    logger.info(f"API基础URL: {settings.API_BASE_URL}")
    logger.info(f"调试模式: {'开启' if args.debug else '关闭'}")
    
    # 启动服务
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
