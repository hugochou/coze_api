"""
文件管理相关API路由
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from core.utils.path_utils import PathUtils
from config import settings

# 创建蓝图
file_bp = Blueprint('file', __name__, url_prefix='/api/file')
path_utils = PathUtils()

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

@file_bp.route('/list', methods=['GET'])
def list_files():
    """
    获取文件列表
    
    查询参数:
    - type: (可选) 文件类型，可选值为 all, image, audio, video
    
    响应:
    {
        "success": true,
        "files": [
            {
                "name": "file1.jpg",
                "path": "/path/to/file1.jpg",
                "url": "/uploads/file1.jpg",
                "full_url": "http://localhost:8000/uploads/file1.jpg",
                "type": "image",
                "size": 1024, // 字节
                "modified": "2024-04-01 12:30:45"
            },
            // ...更多文件
        ]
    }
    """
    try:
        # 获取请求参数
        file_type = request.args.get('type', 'all')
        current_app.logger.info(f"请求获取文件列表，类型: {file_type}")
        
        # 获取数据目录路径
        data_dir = path_utils.get_data_dir()
        current_app.logger.info(f"数据目录路径: {data_dir}")
        current_app.logger.info(f"数据目录是否存在: {data_dir.exists()}")
        
        files = []
        
        # 根据类型获取对应目录
        dirs_to_check = []
        if file_type in ['all', 'image']:
            dirs_to_check.append(('uploads', 'image', '/uploads/'))
        if file_type in ['all', 'audio']:
            dirs_to_check.append(('audio', 'audio', '/audio/'))
        if file_type in ['all', 'video']:
            dirs_to_check.append(('output', 'video', '/videos/'))
        
        current_app.logger.info(f"将检查的目录: {dirs_to_check}")
        
        # 遍历目录获取文件
        for dir_name, type_name, url_prefix in dirs_to_check:
            dir_path = data_dir / dir_name
            current_app.logger.info(f"检查目录: {dir_path}, 文件类型: {type_name}")
            current_app.logger.info(f"目录是否存在: {dir_path.exists()}")
            
            if dir_path.exists():
                # 列出目录内容用于调试
                files_in_dir = list(dir_path.glob('*'))
                current_app.logger.info(f"目录 {dir_path} 中的文件: {[f.name for f in files_in_dir if f.is_file()]}")
                
                for file_path in dir_path.glob('*'):
                    if file_path.is_file():
                        # 跳过隐藏文件和系统文件
                        if file_path.name.startswith('.') or file_path.name == '.DS_Store' or file_path.name == '.gitkeep':
                            current_app.logger.info(f"跳过隐藏文件: {file_path.name}")
                            continue
                        
                        # 获取文件信息
                        stat = file_path.stat()
                        relative_url = f"{url_prefix}{file_path.name}"
                        full_url = get_full_url(relative_url)
                        
                        # 添加文件信息
                        file_info = {
                            'name': file_path.name,
                            'path': str(file_path),
                            'url': relative_url,
                            'full_url': full_url,
                            'type': type_name,
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        }
                        files.append(file_info)
                        current_app.logger.info(f"添加文件: {file_info}")
        
        # 按修改时间降序排序
        files.sort(key=lambda x: x['modified'], reverse=True)
        current_app.logger.info(f"返回文件列表，共 {len(files)} 个文件")
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        current_app.logger.error(f"获取文件列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"获取文件列表失败: {str(e)}"
        }), 500

@file_bp.route('/delete', methods=['POST'])
def delete_files():
    """
    删除文件
    
    请求参数:
    {
        "files": [ // 要删除的文件列表
            "/path/to/file1.jpg",
            "/path/to/file2.mp3"
        ]
    }
    
    响应:
    {
        "success": true,
        "deleted": 2, // 成功删除的文件数量
        "failed": [] // 删除失败的文件路径
    }
    """
    try:
        data = request.json
        if not data or 'files' not in data or not isinstance(data['files'], list):
            return jsonify({
                'success': False,
                'error': "请求参数错误，需要提供文件路径列表"
            }), 400
        
        # 获取数据目录路径
        data_dir = path_utils.get_data_dir()
        current_app.logger.info(f"数据目录路径: {data_dir}")
        
        file_paths = data['files']
        deleted = 0
        failed = []
        
        for file_path in file_paths:
            try:
                # 安全检查：确保路径在data目录下
                path = Path(file_path)
                
                if str(data_dir) in str(path) and path.exists() and path.is_file():
                    path.unlink()
                    deleted += 1
                    current_app.logger.info(f"已删除文件: {path}")
                else:
                    current_app.logger.warning(f"无法删除文件: {path}, 文件不存在或不在数据目录下")
                    failed.append(file_path)
            except Exception as e:
                current_app.logger.error(f"删除文件失败: {file_path} - {str(e)}")
                failed.append(file_path)
        
        return jsonify({
            'success': True,
            'deleted': deleted,
            'failed': failed
        })
        
    except Exception as e:
        current_app.logger.error(f"批量删除文件失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"批量删除文件失败: {str(e)}"
        }), 500

@file_bp.route('/clear', methods=['POST'])
def clear_files():
    """
    清空指定类型的所有文件
    
    请求参数:
    {
        "type": "all" // 文件类型，可选值为 all, image, audio, video
    }
    
    响应:
    {
        "success": true,
        "message": "成功清空所有文件",
        "cleared": {
            "image": 10,
            "audio": 5,
            "video": 3
        }
    }
    """
    try:
        data = request.json
        if not data or 'type' not in data:
            return jsonify({
                'success': False,
                'error': "请求参数错误，需要提供文件类型"
            }), 400
        
        # 获取数据目录路径
        data_dir = path_utils.get_data_dir()
        current_app.logger.info(f"数据目录路径: {data_dir}")
        
        file_type = data['type']
        
        # 根据类型获取对应目录
        dirs_to_clear = []
        if file_type in ['all', 'image']:
            dirs_to_clear.append(('uploads', 'image'))
        if file_type in ['all', 'audio']:
            dirs_to_clear.append(('audio', 'audio'))
        if file_type in ['all', 'video']:
            dirs_to_clear.append(('output', 'video'))
        
        # 清空目录
        cleared = {}
        for dir_name, type_name in dirs_to_clear:
            dir_path = data_dir / dir_name
            if dir_path.exists():
                # 计数并清空
                count = 0
                for file_path in dir_path.glob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        try:
                            file_path.unlink()
                            count += 1
                            current_app.logger.info(f"已删除文件: {file_path}")
                        except Exception as e:
                            current_app.logger.error(f"删除文件失败: {file_path} - {str(e)}")
                
                cleared[type_name] = count
        
        # 生成消息
        message = "成功清空所有文件" if file_type == 'all' else f"成功清空所有{file_type}文件"
        
        return jsonify({
            'success': True,
            'message': message,
            'cleared': cleared
        })
        
    except Exception as e:
        current_app.logger.error(f"清空文件失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"清空文件失败: {str(e)}"
        }), 500 