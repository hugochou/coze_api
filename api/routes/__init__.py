"""
API路由模块
"""

from api.routes.video_routes import video_bp
from api.routes.upload_routes import upload_bp
from api.routes.audio_routes import audio_bp
from api.routes.file_routes import file_bp

# 蓝图列表，每次添加新蓝图都需要更新此列表
blueprints = [
    video_bp,
    upload_bp,
    audio_bp,
    file_bp
]

def register_blueprints(app):
    """
    注册所有路由蓝图到Flask应用
    """
    for bp in blueprints:
        app.register_blueprint(bp)
    return app
