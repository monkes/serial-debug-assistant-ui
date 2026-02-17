#!/bin/bash
# Debug Assistant 启动脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 运行主程序
python3 run.py "$@"
