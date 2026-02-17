# 调试助手

一个支持动态加载插件的调试工具，可以通过添加插件来扩展功能。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-orange.svg)

## 功能特点

- ✨ 支持动态加载Python插件
- 🎨 插件管理界面
- 📝 日志和调试输出窗口
- 🔧 可扩展的插件系统
- 🔒 系统插件和用户插件分离

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/monkes/serial-debug-assistant-ui.git
cd serial-debug-assistant-ui

# 安装依赖（使用系统包管理器）
sudo apt-get install python3-pyqt5 python3-serial python3-pyqt5.sip python3-pyqt5.qtserialport

# 运行程序
python3 run.py

# 或使用启动脚本
./run.sh
```

### 从deb包安装

```bash
# 下载deb包后安装
sudo dpkg -i debug-assistant_<version>-<revision>_all.deb

# 如果有依赖问题，运行
sudo apt-get install -f
```

## 插件管理

1. 启动程序后，左侧会显示插件管理面板
2. 点击"插件"菜单中的"加载插件"可以添加新的插件
3. 在插件列表中选择插件，可以查看插件信息
4. 点击"移除插件"按钮可以卸载选中的插件
5. 新插件会自动复制到用户插件目录 (~/.local/share/debug-assistant/plugins/)

## 开发插件

插件需要继承`PluginInterface`类并实现以下方法：

- `get_name()`: 返回插件名称
- `get_description()`: 返回插件描述
- `get_version()`: 返回插件版本
- `get_author()`: 返回插件作者

可选实现的方法：

- `initialize(main_window)`: 初始化插件
- `activate()`: 激活插件
- `deactivate()`: 停用插件

### 插件目录

- 系统插件目录：`/usr/lib/debug-assistant/plugins/`（需要root权限）
- 用户插件目录：`~/.local/share/debug-assistant/plugins/`（无需root权限）

## 系统要求

- Python 3.6+
- PyQt5 5.15.0+
- PySerial 3.5+

## 文档

详细文档请查看 [文档](./文档) 目录：
- [项目说明](./文档/项目说明.md)
- [API文档](./文档/API文档.md)
- [插件权限说明](./文档/插件权限说明.md)
- [更新日志](./文档/更新日志.md)

## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 作者

Zhang yang

## 贡献

欢迎提交 Issue 和 Pull Request！
