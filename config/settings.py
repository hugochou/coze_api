"""
项目配置文件
"""
import os
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据目录
DATA_DIR = ROOT_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUT_DIR = DATA_DIR / "output"
TEMP_DIR = DATA_DIR / "temp"
AUDIO_DIR = DATA_DIR / "audio"

# API服务设置
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = int(os.environ.get("API_PORT", 8000))
API_BASE_URL = os.environ.get("API_BASE_URL", f"http://{API_HOST}:{API_PORT}")

# 视频服务设置
VIDEO_SETTINGS = {
    "default_fps": 30,
    "default_duration": 5,
    "default_transition": "淡入淡出",
    "default_transition_duration": 0.7,
    "default_quality": "medium"
}

# 音频服务设置
AUDIO_SETTINGS = {
    "language": "zh",
    "speed": 1.0,
}

# 日志配置
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_DIR = ROOT_DIR / "logs"

# 应用设置
APP_NAME = "Image2Video"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Image2Video Team"

# 界面设置
UI_THEME = "fusion"
UI_STYLE = {
    "primaryColor": "#2979ff",
    "secondaryColor": "#f50057",
    "successColor": "#4caf50",
    "warningColor": "#ff9800",
    "errorColor": "#f44336",
    "backgroundColor": "#ffffff",
    "textColor": "#212121",
    "borderRadius": "4px",
    "fontSize": "14px",
    "fontFamily": "Arial, sans-serif"
} 