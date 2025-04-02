from pathlib import Path
import os
import platform
import tempfile
import uuid

class PathUtils:
    """
    路径工具类，处理项目中的各种路径
    """
    
    @staticmethod
    def get_project_root() -> Path:
        """获取项目根目录"""
        # 解决从不同目录启动时路径问题
        current_dir = Path.cwd()
        # 如果当前是在api子目录，则返回其父目录
        if current_dir.name == 'api':
            return current_dir.parent
        # 否则假设当前目录就是项目根目录
        return current_dir
    
    @staticmethod
    def get_data_dir() -> Path:
        """获取数据目录"""
        data_dir = PathUtils.get_project_root() / 'data'
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    
    @staticmethod
    def get_uploads_dir() -> Path:
        """获取上传目录"""
        uploads_dir = PathUtils.get_data_dir() / 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        return uploads_dir
    
    @staticmethod
    def get_output_dir() -> Path:
        """获取输出目录"""
        output_dir = PathUtils.get_data_dir() / 'output'
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    @staticmethod
    def get_temp_dir() -> Path:
        """获取临时目录"""
        temp_dir = PathUtils.get_data_dir() / 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir
    
    @staticmethod
    def get_unique_filename(directory: Path, prefix: str = "", suffix: str = ".mp4") -> Path:
        """
        生成唯一的文件名
        
        Args:
            directory: 文件所在目录
            prefix: 文件名前缀
            suffix: 文件扩展名
            
        Returns:
            唯一的文件路径
        """
        filename = f"{prefix}{uuid.uuid4().hex}{suffix}"
        return directory / filename
    
    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """确保目录存在"""
        os.makedirs(path, exist_ok=True)
        return path 