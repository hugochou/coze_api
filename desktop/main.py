#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片转视频桌面应用程序入口
"""

import sys
import os
from pathlib import Path
import logging
from PyQt6.QtWidgets import QApplication

# 将项目根目录添加到Python路径
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from desktop.ui.main_window import MainWindow

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('desktop-app')

def main():
    """应用程序主入口"""
    try:
        # 创建应用程序实例
        app = QApplication(sys.argv)
        
        # 设置应用程序属性
        app.setApplicationName("Image2Video")
        app.setApplicationDisplayName("图片转视频工具")
        
        # 创建并显示主窗口
        window = MainWindow()
        window.show()
        
        # 进入应用程序主循环
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"应用程序启动失败: {str(e)}")
        raise

if __name__ == "__main__":
    main()
