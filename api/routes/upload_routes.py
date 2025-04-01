from flask import Blueprint, request, jsonify, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import logging
import traceback
from pathlib import Path

from core.utils.path_utils import PathUtils
from config import settings

# 初始化路由蓝图
upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

# 初始化服务
path_utils = PathUtils()

# 设置日志
logger = logging.getLogger("upload-routes")

# 允许的文件类型
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}

def allowed_file(filename, allowed_extensions):
    """检查文件是否有允许的扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_full_url(relative_url):
    """获取完整URL，包含域名和端口
    
    优先使用配置文件中的BASE_URL，如果未配置则使用请求中的主机名
    """
    # 先尝试使用配置文件中的BASE_URL
    if hasattr(settings, 'API_BASE_URL') and settings.API_BASE_URL:
        base_url = settings.API_BASE_URL.rstrip('/')
        return f"{base_url}{relative_url}"
    
    # 如果没有配置，则使用请求的主机名
    host = request.host_url.rstrip('/')
    return f"{host}{relative_url}"

@upload_bp.route('/image', methods=['POST'])
def upload_image():
    """
    上传图片文件
    
    请求体应包含:
        - file: 图片文件
        
    返回:
        上传文件的路径和URL
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({"error": "没有文件"}), 400
            
        file = request.files['file']
        
        # 如果用户没有选择文件
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
            
        # 检查是否是允许的文件类型
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({"error": "不支持的图片格式"}), 400
            
        # 创建文件名并保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        unique_filename = f"{base}_{timestamp}_{uuid.uuid4().hex[:8]}{ext}"
        
        # 获取上传目录
        upload_dir = path_utils.get_uploads_dir()
        file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 相对URL和完整URL
        relative_url = f"/uploads/{unique_filename}"
        full_url = get_full_url(relative_url)
        
        # 返回文件信息
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "path": file_path,
            "url": relative_url,
            "full_url": full_url
        })
        
    except Exception as e:
        logger.error(f"上传图片时出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@upload_bp.route('/audio', methods=['POST'])
def upload_audio():
    """
    上传音频文件
    
    请求体应包含:
        - file: 音频文件
        
    返回:
        上传文件的路径和URL
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({"error": "没有文件"}), 400
            
        file = request.files['file']
        
        # 如果用户没有选择文件
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
            
        # 检查是否是允许的文件类型
        if not allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({"error": "不支持的音频格式"}), 400
            
        # 创建文件名并保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        unique_filename = f"{base}_{timestamp}_{uuid.uuid4().hex[:8]}{ext}"
        
        # 获取上传目录
        upload_dir = path_utils.get_uploads_dir()
        file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 相对URL和完整URL
        relative_url = f"/uploads/{unique_filename}"
        full_url = get_full_url(relative_url)
        
        # 返回文件信息
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "path": file_path,
            "url": relative_url,
            "full_url": full_url
        })
        
    except Exception as e:
        logger.error(f"上传音频时出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 