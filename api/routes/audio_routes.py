"""
音频相关API路由
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from core.services.audio_service import AudioService
from core.utils.path_utils import PathUtils

# 创建蓝图
audio_bp = Blueprint('audio', __name__, url_prefix='/api/audio')
audio_service = AudioService()
path_utils = PathUtils()

@audio_bp.route('/create', methods=['POST'])
def create_audio():
    """
    根据提供的文本创建音频
    
    请求参数:
    - text: 要转换为音频的文本
    - voice: (可选) 语音类型，默认为'zh-cn'
    - speed: (可选) 语速，范围0.5-2.0，默认为1.0
    - format: (可选) 输出格式，默认为'mp3'
    
    响应:
    {
        "success": true,
        "filename": "audio_xxx.mp3",
        "path": "/path/to/audio_xxx.mp3",
        "url": "/audio/audio_xxx.mp3",
        "full_url": "http://localhost:8000/audio/audio_xxx.mp3"
    }
    """
    try:
        # 获取请求数据
        data = request.json
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "缺少必要参数 'text'"
            }), 400
        
        text = data['text']
        voice = data.get('voice', 'zh-cn')  # 默认中文
        speed = data.get('speed', 1.0)  # 默认语速1.0
        format_type = data.get('format', 'mp3')  # 默认格式mp3
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = str(uuid.uuid4())[:8]
        filename = f"audio_{timestamp}_{random_str}.{format_type}"
        
        # 确保音频目录存在
        audio_dir = os.path.join(os.getcwd(), "data", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        # 生成音频文件
        # 注意：目前AudioService实现只支持中文，并使用mp3格式
        # 如果需要支持更多参数，需要扩展AudioService
        audio_path = audio_service.generate_speech(text, filename)
        
        if not audio_path:
            return jsonify({
                "success": False,
                "error": "音频生成失败"
            }), 500
        
        # 构建URL路径 - 使用/audio/路径而不是/uploads/
        relative_path = f"/audio/{os.path.basename(audio_path)}"
        from config import settings
        full_url = f"{settings.API_BASE_URL}{relative_path}"
        
        return jsonify({
            "success": True,
            "filename": os.path.basename(audio_path),
            "path": str(audio_path),
            "url": relative_path,
            "full_url": full_url
        })
        
    except Exception as e:
        current_app.logger.error(f"创建音频失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"创建音频失败: {str(e)}"
        }), 500 