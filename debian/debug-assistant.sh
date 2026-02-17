#!/bin/bash
# Debug Assistant 启动脚本

# 设置PYTHONPATH
export PYTHONPATH=/usr/lib/debug-assistant:$PYTHONPATH

# 切换到程序目录
cd /usr/lib/debug-assistant

# 运行主程序
python3 main.py "$@"
