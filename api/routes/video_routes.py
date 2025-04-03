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
        transition = request_data.get('transition', '')
        if not transition:
            transition = '随机'
            logger.info("未提供转场效果类型，使用随机效果")
            
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

@video_bp.route('/image2video', methods=['POST'])
def image2video():
    """
    从单张图片和音频创建视频
    
    请求体应包含:
        - image_path: 图片路径
        - audio_path: 音频路径
        - animation_scale: 缩放动画类型（"无", "放大", "缩小"等，AnimationService中的预设）
        - animation_position: 平移动画类型（"无", "左到右", "右到左"等，AnimationService中的预设）
        - animation_curve: 动画曲线类型（"线性", "缓入", "缓出"等，AnimationService中的预设）
        - output_fps: 输出视频帧率（默认30）
        - output_quality: 输出视频质量（low/medium/high）
    
    返回:
        视频文件的URL
    """
    try:
        # 获取请求数据
        request_data = request.json
        if not request_data:
            return jsonify({"error": "未提供有效的请求数据"}), 400
        
        # 获取图片路径
        image_path = request_data.get('image_path')
        if not image_path:
            return jsonify({"error": "未提供图片路径"}), 400
            
        # 如果是URL格式，尝试将其转换为本地文件路径
        if image_path.startswith('http://') or image_path.startswith('https://'):
            # 提取URL中的文件名部分
            url_parts = image_path.split('/')
            filename = url_parts[-1]
            
            # 查找本地对应的文件
            if '/uploads/' in image_path:
                local_path = os.path.join(path_utils.get_uploads_dir(), filename)
            elif '/audio/' in image_path:
                local_path = os.path.join(path_utils.get_data_dir(), 'audio', filename)
            elif '/videos/' in image_path:
                local_path = os.path.join(path_utils.get_output_dir(), filename)
            else:
                return jsonify({"error": f"无法处理的URL格式路径: {image_path}"}), 400
                
            logger.info(f"将URL路径 {image_path} 转换为本地路径 {local_path}")
            image_path = local_path
            
        # 检查图片路径是否存在
        if not os.path.exists(image_path):
            return jsonify({"error": f"图片文件不存在: {image_path}"}), 400
        
        # 获取音频路径
        audio_path = request_data.get('audio_path')
        if not audio_path:
            return jsonify({"error": "未提供音频路径"}), 400
            
        # 如果是URL格式，尝试将其转换为本地文件路径
        if audio_path.startswith('http://') or audio_path.startswith('https://'):
            # 提取URL中的文件名部分
            url_parts = audio_path.split('/')
            filename = url_parts[-1]
            
            # 查找本地对应的文件
            if '/uploads/' in audio_path:
                local_path = os.path.join(path_utils.get_uploads_dir(), filename)
            elif '/audio/' in audio_path:
                local_path = os.path.join(path_utils.get_data_dir(), 'audio', filename)
            elif '/videos/' in audio_path:
                local_path = os.path.join(path_utils.get_output_dir(), filename)
            else:
                return jsonify({"error": f"无法处理的URL格式路径: {audio_path}"}), 400
                
            logger.info(f"将URL路径 {audio_path} 转换为本地路径 {local_path}")
            audio_path = local_path
            
        # 检查音频路径是否存在
        if not os.path.exists(audio_path):
            return jsonify({"error": f"音频文件不存在: {audio_path}"}), 400
        
        # 获取动画设置
        animation_scale = request_data.get('animation_scale', '')
        if not animation_scale:
            animation_scale = '随机'
            logger.info("未提供缩放动画类型，使用随机效果")
            
        animation_position = request_data.get('animation_position', '')
        if not animation_position:
            animation_position = '随机'
            logger.info("未提供平移动画类型，使用随机效果")
            
        animation_curve = request_data.get('animation_curve', '')
        if not animation_curve:
            animation_curve = '随机'
            logger.info("未提供动画曲线类型，使用随机效果")
        
        # 获取输出设置
        output_fps_value = request_data.get('output_fps', 30)
        if output_fps_value == '':
            output_fps = 30
            logger.info("未提供输出帧率，使用默认值: 30fps")
        else:
            output_fps = int(output_fps_value)
        output_quality = request_data.get('output_quality', 'medium')
        
        # 创建自定义动画设置
        animation = video_service.animation_service.combine_animation_settings(
            animation_scale, 
            animation_position, 
            animation_curve
        )
        
        # 创建图片项
        image_item = {
            'id': str(uuid.uuid4())[:8],
            'image_path': image_path,
            'audio_path': audio_path,
            'animation': animation
        }
        
        # 创建输出目录
        output_dir = path_utils.get_output_dir()
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"image2video_{timestamp}_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        # 创建视频
        logger.info(f"开始创建单图视频，图片: {image_path}, 音频: {audio_path}")
        
        result_path = video_service.create_video(
            items=[image_item],
            output_path=output_path,
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
            "message": "单图音频视频创建成功"
        })
        
    except Exception as e:
        logger.error(f"创建单图视频时出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@video_bp.route('/videos2video', methods=['POST'])
def videos2video():
    """
    将多段视频合并成一个视频
    
    请求体应包含:
        - video_paths: 视频路径列表
        - transition: 转场效果名称（TransitionService中的预设）
        - transition_duration: 转场持续时间（秒）
        - output_fps: 输出视频帧率（可选，默认使用第一个视频的帧率）
        - output_quality: 输出视频质量（low/medium/high）
    
    返回:
        合并后的视频文件URL
    """
    try:
        # 获取请求数据
        request_data = request.json
        if not request_data:
            return jsonify({"error": "未提供有效的请求数据"}), 400
        
        # 获取视频路径列表
        video_paths = request_data.get('video_paths', [])
        if not video_paths:
            return jsonify({"error": "未提供视频路径列表"}), 400
        
        # 处理路径列表，将URL转换为本地路径
        processed_paths = []
        for i, path in enumerate(video_paths):
            if path.startswith('http://') or path.startswith('https://'):
                # 提取URL中的文件名部分
                url_parts = path.split('/')
                filename = url_parts[-1]
                
                # 查找本地对应的文件
                if '/uploads/' in path:
                    local_path = os.path.join(path_utils.get_uploads_dir(), filename)
                elif '/audio/' in path:
                    local_path = os.path.join(path_utils.get_data_dir(), 'audio', filename)
                elif '/videos/' in path:
                    local_path = os.path.join(path_utils.get_output_dir(), filename)
                else:
                    return jsonify({"error": f"无法处理的URL格式路径: {path}"}), 400
                    
                logger.info(f"将URL路径 {path} 转换为本地路径 {local_path}")
                processed_paths.append(local_path)
            else:
                processed_paths.append(path)
        
        # 检查所有视频路径是否有效
        for i, path in enumerate(processed_paths):
            if not os.path.exists(path):
                return jsonify({"error": f"视频文件不存在: {path} (原始路径: {video_paths[i]})"}), 400
        
        # 更新使用处理后的路径列表
        video_paths = processed_paths
        
        # 获取转场设置
        transition = request_data.get('transition', '')
        if not transition:
            transition = '随机'
            logger.info("未提供转场效果类型，使用随机效果")
            
        transition_duration = float(request_data.get('transition_duration', 0.7))
        
        # 获取输出设置
        output_fps_value = request_data.get('output_fps')
        if output_fps_value == '':
            output_fps = 30
            logger.info("未提供输出帧率，使用默认值: 30fps")
        else:
            output_fps = int(output_fps_value)
        output_quality = request_data.get('output_quality', 'medium')
        
        # 创建输出目录
        output_dir = path_utils.get_output_dir()
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"videos2video_{timestamp}_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        # 合并视频
        logger.info(f"开始合并视频，视频数量: {len(video_paths)}, 转场: {transition}")
        
        result_path = video_service.combine_videos(
            video_paths=video_paths,
            output_path=output_path,
            transition=transition,
            transition_duration=transition_duration,
            output_fps=output_fps,
            output_quality=output_quality
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
            "message": "视频合并成功"
        })
        
    except Exception as e:
        logger.error(f"合并视频时出错: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 