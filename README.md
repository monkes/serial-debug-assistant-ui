# 调试助手

## 项目概述

调试助手是一个基于 Python 3 和 PyQt5 开发的通用调试工具，采用插件化架构设计，支持动态加载插件来扩展功能。项目旨在为开发者提供一个灵活、可扩展的调试平台，通过插件机制实现功能的模块化和可定制化。
- 主项目：https://github.com/monkes/serial-debug-assistant-ui.git
- 插件仓库：https://github.com/monkes/serial-debug-assistant-plugins.git

## 核心特性

### 1. 插件化架构
- **动态加载**：支持运行时动态加载和卸载 Python 插件
- **插件管理**：提供直观的插件管理界面，方便用户管理插件
- **权限分离**：系统插件和用户插件分离，确保系统安全和用户便利性
- **可扩展性**：基于 `PluginInterface` 接口，开发者可以轻松创建自定义插件

### 2. 用户界面
- **现代化界面**：基于 PyQt5 构建的现代化图形用户界面
- **多标签页**：支持多标签页工作模式，便于同时处理多个任务
- **日志窗口**：内置日志和调试输出窗口，实时显示程序运行信息
- **状态栏**：底部状态栏显示程序状态和提示信息

### 3. 插件系统
- **标准接口**：提供统一的插件接口规范
- **生命周期管理**：完整的插件生命周期管理（初始化、激活、停用）
- **元数据支持**：支持插件名称、描述、版本、作者等元数据
- **热加载**：无需重启程序即可加载新插件

### 4. 系统集成
- **桌面集成**：支持从应用程序菜单启动
- **命令行支持**：提供命令行工具 `debug-assistant`
- **多平台支持**：支持 Linux 系统，可打包为 deb 包分发

## 技术栈

- **编程语言**：Python 3.6+
- **GUI框架**：PyQt5
- **串口通信**：PySerial
- **打包工具**：Debian 打包系统

## 项目结构

```
debug-assistant/
├── debug_assistant/       # 主程序包
│   ├── main.py           # 程序入口
│   ├── main_window.py    # 主窗口实现
│   ├── plugin_manager.py # 插件管理器
│   ├── plugin_interface.py # 插件接口
│   ├── plugins/          # 插件目录
│   └── resources/        # 资源文件
├── debian/               # Debian 打包文件
├── build_output/         # 构建输出目录
├── 文档/                # 项目文档
│   ├── 项目说明.md
│   ├── API文档.md
│   ├── 插件权限说明.md
│   └── 更新日志.md
└── build.sh             # 构建脚本
```

## 使用场景

1. **串口调试**：通过插件实现串口通信调试功能
2. **协议分析**：开发协议分析插件，支持各种通信协议
3. **数据监控**：实时监控和分析数据流
4. **自动化测试**：编写测试插件，实现自动化测试流程
5. **自定义工具**：根据特定需求开发自定义调试工具

## 系统要求

- Python 3.6+
- PyQt5
- PySerial

## 安装

### 从源码安装

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

#### 构建deb包

```bash
# 克隆仓库
git clone https://github.com/monkes/serial-debug-assistant-ui.git
cd serial-debug-assistant-ui

# 构建deb包
./build.sh

# 构建产物位于 build_output/ 目录
ls build_output/
```

#### 安装deb包

```bash
# 安装deb包（构建产物位于 build_output/ 目录）
sudo dpkg -i build_output/debug-assistant_<version>-<revision>_all.deb

# 如果有依赖问题，运行
sudo apt-get install -f
```

> 注意：
> - `<version>` 替换为实际版本号（如：1.0.0）
> - `<revision>` 替换为修订号（如：0）
> - 完整示例：`debug-assistant_1.0.0-0_all.deb`

## 使用说明

### 开发环境

在开发环境中，可以使用以下方式启动程序：

```bash
# 使用Python直接运行
python3 run.py

# 或使用启动脚本
./run.sh
```

### 安装后环境

在安装后的环境中，可以使用以下方式启动程序：

```bash
# 使用命令行
debug-assistant

# 或从应用程序菜单启动
```

### 插件管理

1. 启动程序后，左侧会显示插件管理面板
2. 点击"插件"菜单中的"加载插件"可以添加新的插件
3. 在插件列表中选择插件，可以查看插件信息
4. 点击"移除插件"按钮可以卸载选中的插件
5. 新插件会自动复制到用户插件目录 (~/.local/share/debug-assistant/plugins/)
6. 详见插件权限说明.md了解插件权限管理机制

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

- 系统插件目录：`/usr/lib/debug-assistant/debug_assistant/plugins/`（需要root权限）
- 用户插件目录：`~/.local/share/debug-assistant/plugins/`（无需root权限）

详见插件权限说明.md了解插件权限管理机制

## 许可证

MIT License

## 作者

Zhang yang

## 版本

1.0.0

## 项目地址

- 主项目：https://github.com/monkes/serial-debug-assistant-ui.git
- 插件仓库：https://github.com/monkes/serial-debug-assistant-plugins.git
