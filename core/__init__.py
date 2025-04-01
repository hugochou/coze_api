"""
Image2Video 核心模块

此模块包含所有核心业务逻辑，独立于界面和API服务。
"""

__version__ = '1.0.0'

# 导出所有子模块
from core import models
from core import services
from core import utils

__all__ = ['models', 'services', 'utils']
