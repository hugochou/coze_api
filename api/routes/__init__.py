"""
API路由模块
"""

from api.routes.video_routes import video_bp
from api.routes.upload_routes import upload_bp

# 路由蓝图列表
blueprints = [
    video_bp,
    upload_bp
]

def register_blueprints(app):
    """
    注册所有路由蓝图到Flask应用
    
    Args:
        app: Flask应用实例
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
