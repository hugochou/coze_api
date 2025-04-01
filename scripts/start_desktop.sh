#!/bin/bash

# 切换到项目根目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
  echo "创建虚拟环境..."
  python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "警告: 未找到requirements.txt文件"
fi

# 启动桌面应用
echo "启动 Image2Video 桌面应用"
python -m desktop.main 