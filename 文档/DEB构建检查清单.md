# DEB包构建检查清单

## 打包前检查

### 1. 必需文件检查
- [x] debug_assistant/main.py - 主程序
- [x] debug_assistant/main_window.py - 主窗口
- [x] debug_assistant/plugin_interface.py - 插件接口
- [x] debug_assistant/plugin_manager.py - 插件管理器
- [x] debug_assistant/requirements.txt - 依赖列表
- [x] README.md - 项目说明
- [x] LICENSE - 许可证
- [x] setup.py - Python包配置
- [x] MANIFEST.in - 打包清单
- [x] PACKAGING.md - 打包说明文档
- [x] run.py - 主入口文件

### 2. Debian打包文件检查
- [x] debian/control - 包控制信息
- [x] debian/rules - 构建规则
- [x] debian/changelog - 变更日志
- [x] debian/install - 安装文件列表
- [x] debian/debug-assistant.sh - 启动脚本

### 3. 资源文件检查
- [x] debug_assistant/resources/icon256x256.png - 256x256图标
- [x] debug_assistant/resources/icon128x128.png - 128x128图标
- [x] debug_assistant/resources/icon64x64.png - 64x64图标
- [x] debug_assistant/resources/icon48x48.png - 48x48图标

### 4. 桌面集成文件检查
- [x] share/applications/debug-assistant.desktop - 桌面文件

### 5. 插件目录检查
- [x] plugins/ - 系统插件目录（可为空）
- [x] 用户插件目录将在首次运行时自动创建 (~/.local/share/debug-assistant/plugins/)

## 依赖项检查

### Python依赖
- [x] PyQt5>=5.15.0
- [x] PyQt5-Qt5>=5.15.0
- [x] PyQt5-sip>=12.8.0
- [x] pyqt5-tools>=5.15.0
- [x] PySerial>=3.5
- [x] pyqt5-qt5serialport>=5.15.0

### 系统依赖（debian/control）
- [x] python3-pyqt5
- [x] python3-serial

## 构建环境检查

### 必需工具
- [x] debhelper (>=13)
- [x] dh-python
- [x] python3-setuptools
- [x] python3-all

## 构建前准备

1. 确保所有图标文件已添加到debug_assistant/resources目录
2. 检查debian/rules中的路径是否正确
3. 确保debian/control中的依赖项完整
4. 验证debian/changelog的格式正确
5. 确保debian/rules文件有执行权限

## 构建命令

```bash
# 方法1：使用debuild
debuild -us -uc

# 方法2：使用dpkg-buildpackage
dpkg-buildpackage -us -uc

# 方法3：使用构建脚本
./build.sh
```

## 安装测试

```bash
# 安装包
sudo dpkg -i ../debug-assistant_1.0.0_all.deb

# 修复依赖
sudo apt-get install -f

# 测试运行
debug-assistant

# 检查桌面集成
ls /usr/share/applications/debug-assistant.desktop
ls /usr/share/icons/hicolor/*/apps/debug-assistant.png

# 卸载
sudo apt-get remove debug-assistant
```

## 常见问题

1. **图标未显示**
   - 检查图标文件是否存在
   - 运行 `gtk-update-icon-cache` 更新图标缓存

2. **启动失败**
   - 检查启动脚本权限
   - 查看日志文件了解错误信息

3. **依赖问题**
   - 确保debian/control中列出了所有必需的依赖
   - 运行 `apt-get install -f` 修复依赖

4. **插件加载失败**
   - 检查系统插件目录权限
   - 检查用户插件目录是否正确创建
   - 确保插件文件实现了正确的接口

5. **插件权限问题**
   - 系统插件目录需要root权限才能修改
   - 用户插件目录在首次运行时自动创建
   - 新插件会自动复制到用户插件目录
   - 详见插件权限说明.md
