from flask import Blueprint, request, jsonify, send_file, abort
import os
import json
import uuid
from pathlib import Path
from datetime import datetime
import traceback
import logging

from core.models.image_item import ImageItem
from core.services.video_service import VideoService
from core.utils.path_utils import PathUtils
from config import settings

# 初始化路由蓝图
video_bp = Blueprint('video', __name__, url_prefix='/api/video')

# 初始化服务
video_service = VideoService()
path_utils = PathUtils()

# 设置日志
logger = logging.getLogger("video-routes")

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

@video_bp.route('/create', methods=['POST'])
def create_video():
    """
    从上传的图片数据创建视频
    
    请求体应包含:
        - images: 图片项列表，每个包含id, image_path, duration, animation等
        - transition: 转场效果名称
        - transition_duration: 转场持续时间
        - output_fps: 输出视频帧率
        - output_quality: 输出视频质量
    
    返回:
        视频文件的URL
    """
    try:
        # 获取请求数据
        request_data = request.json
        if not request_data:
            return jsonify({"error": "未提供有效的请求数据"}), 400
        
        # 获取图片列表
        images_data = request_data.get('images', [])
        if not images_data:
            return jsonify({"error": "未提供图片数据"}), 400
        
        # 确保所有图片路径都存在
        for img in images_data:
            img_path = img.get('image_path')
            if not img_path or not os.path.exists(img_path):
                return jsonify({"error": f"图片路径无效或不存在: {img_path}"}), 400
        
        # 获取转场和输出设置
        transition = request_data.get('transition', '淡入淡出')
        transition_duration = float(request_data.get('transition_duration', 0.7))
        output_fps = int(request_data.get('output_fps', 30))
        output_quality = request_data.get('output_quality', 'medium')
        
        # 创建输出目录
        output_dir = path_utils.get_output_dir()
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"video_{timestamp}_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        # 创建视频
        logger.info(f"开始创建视频，图片数: {len(images_data)}, 转场: {transition}")
        
        result_path = video_service.create_video(
            items=images_data,
            output_path=output_path,
            transition=transition,
            transition_duration=transition_duration,
            advanced_options={
                'output_quality': output_quality
            }
        )
        
        # 获取实际生成的文件名
        actual_filename = os.path.basename(result_path)
        # 返回结果
        relative_url = f"/videos/{actual_filename}"
        full_url = get_full_url(relative_url)
        
        return jsonify({
            "success": True,
            "video_path": result_path,
            "video_url": relative_url,
            "video_full_url": full_url,
            "message": "视频创建成功"
        })
        
    except Exception as e:
        logger.error(f"创建视频时出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@video_bp.route('/list', methods=['GET'])
def list_videos():
    """
    列出所有已生成的视频
    
    返回:
        视频列表，每个包含路径和URL
    """
    try:
        output_dir = path_utils.get_output_dir()
        video_files = [f for f in os.listdir(output_dir) 
                       if f.endswith('.mp4') and os.path.isfile(os.path.join(output_dir, f))]
        
        videos = []
        for filename in video_files:
            # 获取文件信息
            file_path = os.path.join(output_dir, filename)
            file_size = os.path.getsize(file_path)
            mod_time = os.path.getmtime(file_path)
            create_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # 构建URL
            relative_url = f"/videos/{filename}"
            full_url = get_full_url(relative_url)
            
            videos.append({
                "filename": filename,
                "path": file_path,
                "url": relative_url,
                "full_url": full_url,
                "size": file_size,
                "created_at": create_time
            })
        
        # 按修改时间倒序排序
        videos.sort(key=lambda x: x["created_at"], reverse=True)
        
        return jsonify({
            "success": True,
            "videos": videos
        })
        
    except Exception as e:
        logger.error(f"列出视频时出错: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@video_bp.route('/get/<filename>', methods=['GET'])
def get_video(filename):
    """
    获取指定的视频文件
    
    路径参数:
        - filename: 视频文件名
    
    返回:
        视频文件
    """
    try:
        output_dir = path_utils.get_output_dir()
        video_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(video_path):
            abort(404, f"视频文件 {filename} 不存在")
        
        return send_file(video_path, mimetype='video/mp4')
        
    except Exception as e:
        logger.error(f"获取视频时出错: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 