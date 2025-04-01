#!/bin/bash

# 切换到项目根目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

# 默认值
PORT=8000
HOST="0.0.0.0"
DEBUG=0
BASE_URL=""

# 解析命令行参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --port=*)
      PORT="${1#*=}"
      shift
      ;;
    --host=*)
      HOST="${1#*=}"
      shift
      ;;
    --base-url=*)
      BASE_URL="${1#*=}"
      shift
      ;;
    --debug)
      DEBUG=1
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

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

# 设置环境变量
if [ -n "$BASE_URL" ]; then
  export API_BASE_URL="$BASE_URL"
  echo "设置API_BASE_URL为: $API_BASE_URL"
else
  # 如果没有明确设置BASE_URL，但使用了非默认的HOST
  if [ "$HOST" != "0.0.0.0" ] && [ "$HOST" != "localhost" ]; then
    export API_BASE_URL="http://$HOST:$PORT"
    echo "根据HOST和PORT自动设置API_BASE_URL为: $API_BASE_URL"
  fi
fi

# 启动API服务
echo "启动 Image2Video API 服务，端口: $PORT, 主机: $HOST"

if [ $DEBUG -eq 1 ]; then
  python -m api.app --port=$PORT --host=$HOST --debug
else
  python -m api.app --port=$PORT --host=$HOST
fi 