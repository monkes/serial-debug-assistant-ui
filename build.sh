#!/bin/bash
# Debug Assistant 构建脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 创建构建输出目录
BUILD_OUTPUT_DIR="$SCRIPT_DIR/build_output"
mkdir -p "$BUILD_OUTPUT_DIR"

# 构建Debian包
echo "开始构建Debian包..."
dpkg-buildpackage -us -uc -ui -b

# 移动构建产物到输出目录
echo "移动构建产物到输出目录..."
# 移动当前目录中的.deb文件
mv debug-assistant_*.deb "$BUILD_OUTPUT_DIR/" 2>/dev/null
# 移动父目录中的.deb文件
mv ../debug-assistant_*.deb "$BUILD_OUTPUT_DIR/" 2>/dev/null
# 清理其他构建产物
rm -f debug-assistant_*.build debug-assistant_*.buildinfo debug-assistant_*.changes debug-assistant_*.dsc debug-assistant_*.tar.gz
rm -f ../debug-assistant_*.build ../debug-assistant_*.buildinfo ../debug-assistant_*.changes ../debug-assistant_*.dsc ../debug-assistant_*.tar.gz

# 切换回脚本目录
cd "$SCRIPT_DIR"

# 清理临时文件和编译过的文件
echo "清理临时文件和编译过的文件..."
rm -rf build/ dist/ *.egg-info __pycache__ debug_assistant/__pycache__ debug_assistant/plugins/__pycache__ *.pyc .pytest_cache
rm -rf debian/.debhelper debian/debhelper-build-stamp debian/files debian/debug-assistant/ debian/debug-assistant.substvars
rm -rf "$BUILD_OUTPUT_DIR"/*.buildinfo
echo "构建和清理完成！"
echo "构建产物已保存到: $BUILD_OUTPUT_DIR"
echo "如果需要安装，请运行: sudo dpkg -i $BUILD_OUTPUT_DIR/debug-assistant_*.deb"
