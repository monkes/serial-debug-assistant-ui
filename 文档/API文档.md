# 调试助手 API 文档

## 目录

1. [概述](#概述)
2. [核心模块](#核心模块)
   - [debug_assistant/main.py](#mainpy)
   - [debug_assistant/main_window.py](#main_windowpy)
   - [debug_assistant/plugin_interface.py](#plugin_interfacepy)
   - [debug_assistant/plugin_manager.py](#plugin_managerpy)
3. [插件开发指南](#插件开发指南)
4. [API 参考](#api-参考)

## 概述

调试助手是一个基于Python3和PyQt5开发的可扩展调试工具，采用插件化架构，支持动态加载和卸载插件。本文档详细介绍了调试助手的核心模块、插件接口以及如何开发自定义插件。

## 核心模块

### debug_assistant/main.py

主程序入口文件，负责应用程序的初始化和启动。

#### 函数

##### `main()`

应用程序的主入口函数，负责创建QApplication实例、设置应用程序属性、创建主窗口并启动事件循环。

**功能：**
- 创建QApplication实例
- 设置应用程序名称、组织名称和显示名称
- 设置应用程序图标
- 创建并显示主窗口
- 启动应用程序事件循环

**返回值：** 无

**示例：**
```python
if __name__ == "__main__":
    main()
```

### debug_assistant/main_window.py

主窗口类，实现应用程序的主要用户界面和插件管理功能。

#### 类

##### `MainWindow(QMainWindow)`

主窗口类，继承自QMainWindow，提供应用程序的主要界面和功能。

**属性：**
- `plugin_manager`: PluginManager实例，用于管理插件
- `loaded_plugins`: dict，已加载的插件字典 {plugin_name: plugin_instance}
- `plugin_list`: QListWidget，显示已加载插件列表
- `plugin_info`: QTextEdit，显示选中插件的详细信息
- `remove_plugin_button`: QPushButton，用于移除选中的插件
- `tab_widget`: QTabWidget，中央选项卡控件
- `log_widget`: QTextEdit，日志输出控件
- `debug_output`: QTextEdit，调试输出控件

**方法：**

##### `__init__()`

初始化主窗口。

**功能：**
- 初始化插件管理器
- 初始化已加载插件字典
- 初始化用户界面
- 加载插件

##### `init_ui()`

初始化用户界面。

**功能：**
- 创建菜单栏
- 创建工具栏
- 创建状态栏
- 创建中央部件
- 创建插件管理面板

##### `create_menu_bar()`

创建菜单栏。

**功能：**
- 创建文件菜单，包含退出选项
- 创建插件菜单，包含加载插件选项和已加载插件的快捷方式
- 创建帮助菜单，包含关于选项

##### `create_toolbar()`

创建工具栏。

**功能：**
- 创建主工具栏（当前为空，可根据需要添加按钮）

##### `create_central_widget()`

创建中央部件。

**功能：**
- 创建主分割器
- 创建日志窗口
- 创建调试输出窗口
- 创建选项卡，包含调试输出和日志选项卡
- 设置中央部件

##### `create_plugin_panel()`

创建插件管理面板。

**功能：**
- 创建插件列表
- 创建插件信息面板
- 创建移除插件按钮
- 创建插件面板分割器
- 创建插件面板Dock

##### `load_plugins()`

加载插件目录中的所有插件。

**功能：**
- 获取插件目录
- 如果插件目录不存在，则创建
- 加载插件目录中的所有插件
- 将插件添加到插件列表

**参数：** 无

**返回值：** 无

##### `load_plugin_from_file()`

从文件加载插件。

**功能：**
- 打开文件选择对话框
- 获取插件目录
- 如果插件目录不存在，则创建
- 获取插件文件名和插件名称
- 检查插件是否已存在
- 复制插件文件到plugins目录
- 加载插件
- 将插件添加到插件列表

**参数：** 无

**返回值：** 无

##### `add_plugin_to_list(name, plugin)`

添加插件到列表。

**参数：**
- `name`: str，插件名称
- `plugin`: PluginInterface，插件实例

**功能：**
- 获取插件的显示名称
- 创建列表项
- 将列表项添加到插件列表
- 将插件添加到已加载插件字典
- 创建插件菜单项
- 初始化插件

**返回值：** 无

##### `remove_plugin(name)`

移除插件。

**参数：**
- `name`: str，插件名称

**功能：**
- 停用插件
- 从插件列表中移除
- 从菜单中移除
- 从选项卡中移除（如果插件创建了选项卡）
- 从已加载插件字典中移除

**返回值：** 无

##### `remove_selected_plugin()`

移除选中的插件。

**功能：**
- 获取当前选中的插件
- 查找插件名称
- 确认是否移除插件
- 移除插件文件
- 调用remove_plugin方法移除插件
- 禁用移除插件按钮

**参数：** 无

**返回值：** 无

##### `on_plugin_selected(item)`

插件选择事件处理。

**参数：**
- `item`: QListWidgetItem，选中的列表项

**功能：**
- 获取插件实例
- 显示插件信息
- 启用移除插件按钮

**返回值：** 无

##### `log_message(message)`

记录日志消息。

**参数：**
- `message`: str，日志消息

**功能：**
- 将消息添加到日志窗口
- 自动滚动到底部

**返回值：** 无

##### `debug_message(message)`

记录调试消息。

**参数：**
- `message`: str，调试消息

**功能：**
- 将消息添加到调试输出窗口
- 自动滚动到底部

**返回值：** 无

##### `show_about()`

显示关于对话框。

**功能：**
- 显示应用程序的关于信息

**参数：** 无

**返回值：** 无

### debug_assistant/plugin_interface.py

插件接口定义，所有插件必须实现此接口。

#### 类

##### `PluginInterface(ABC)`

插件接口基类，所有插件必须继承此类并实现其抽象方法。

**抽象方法：**

##### `get_name()`

获取插件名称。

**参数：** 无

**返回值：** str，插件名称

**示例：**
```python
def get_name(self):
    return "我的插件"
```

##### `get_description()`

获取插件描述。

**参数：** 无

**返回值：** str，插件描述

**示例：**
```python
def get_description(self):
    return "这是一个示例插件"
```

##### `get_version()`

获取插件版本。

**参数：** 无

**返回值：** str，插件版本号

**示例：**
```python
def get_version(self):
    return "1.0.0"
```

##### `get_author()`

获取插件作者。

**参数：** 无

**返回值：** str，插件作者

**示例：**
```python
def get_author(self):
    return "您的名字"
```

**可选方法：**

##### `initialize(main_window)`

初始化插件。

**参数：**
- `main_window`: MainWindow，主窗口实例

**功能：**
- 插件初始化时调用
- 可以通过main_window访问主窗口的功能
- 例如：main_window.tab_widget.addTab(widget, "插件名称")

**返回值：** 无

**示例：**
```python
def initialize(self, main_window):
    # 创建插件界面
    self.widget = QWidget()
    layout = QVBoxLayout(self.widget)
    # 添加控件到布局
    # 将插件界面添加到主窗口选项卡
    main_window.tab_widget.addTab(self.widget, self.get_name())
```

##### `activate()`

激活插件。

**参数：** 无

**功能：**
- 激活插件时调用
- 例如：切换到插件的选项卡

**返回值：** 无

**示例：**
```python
def activate(self):
    # 切换到插件的选项卡
    index = self.main_window.tab_widget.indexOf(self.widget)
    if index >= 0:
        self.main_window.tab_widget.setCurrentIndex(index)
```

##### `deactivate()`

停用插件。

**参数：** 无

**功能：**
- 停用插件时调用
- 清理插件资源
- 例如：关闭打开的连接或释放资源

**返回值：** 无

**示例：**
```python
def deactivate(self):
    # 关闭打开的连接
    if hasattr(self, 'connection') and self.connection:
        self.connection.close()
```

### debug_assistant/plugin_manager.py

插件管理器，负责插件的加载、卸载和管理。

#### 类

##### `PluginManager`

插件管理器类，提供插件加载、卸载和查询功能。

**属性：**
- `plugins`: dict，已加载的插件字典 {plugin_name: plugin_instance}

**方法：**

##### `__init__()`

初始化插件管理器。

**功能：**
- 初始化插件字典
- 设置系统插件目录
- 设置用户插件目录
- 确保用户插件目录存在

##### `load_plugins_from_dir(directory)`

从目录加载所有插件。

**参数：**
- `directory`: str，插件目录路径

**返回值：** dict，加载的插件字典 {plugin_name: plugin_instance}

**功能：**
- 如果目录不存在，返回空字典
- 遍历目录中的所有Python文件
- 加载每个插件文件
- 返回加载的插件字典

**示例：**
```python
plugins = plugin_manager.load_plugins_from_dir("/path/to/plugins")
```

##### `load_plugin_from_file(file_path)`

从文件加载插件。

**参数：**
- `file_path`: str，插件文件路径

**返回值：** PluginInterface，插件实例，如果加载失败则返回None

**功能：**
- 获取插件名称
- 如果插件已经加载，则返回已加载的插件
- 动态导入插件模块
- 查找插件类
- 创建插件实例
- 添加到插件字典

**示例：**
```python
plugin = plugin_manager.load_plugin_from_file("/path/to/plugin.py")
```

##### `get_plugin(name)`

获取插件实例。

**参数：**
- `name`: str，插件名称

**返回值：** PluginInterface，插件实例，如果插件不存在则返回None

**示例：**
```python
plugin = plugin_manager.get_plugin("my_plugin")
```

##### `unload_plugin(name)`

卸载插件。

**参数：**
- `name`: str，插件名称

**返回值：** bool，是否成功卸载

**功能：**
- 调用插件的deactivate方法
- 从插件字典中移除插件

**示例：**
```python
success = plugin_manager.unload_plugin("my_plugin")
```

##### `get_all_plugins()`

获取所有插件。

**参数：** 无

**返回值：** dict，所有插件字典 {plugin_name: plugin_instance}

**示例：**
```python
all_plugins = plugin_manager.get_all_plugins()
```

## 插件开发指南

### 创建插件

1. 在`plugins`目录中创建一个新的Python文件

2. 创建一个继承自`PluginInterface`的类：

```python
from plugin_interface import PluginInterface

class MyPlugin(PluginInterface):
    def get_name(self):
        """获取插件名称"""
        return "我的插件"

    def get_description(self):
        """获取插件描述"""
        return "这是一个示例插件"

    def get_version(self):
        """获取插件版本"""
        return "1.0.0"

    def get_author(self):
        """获取插件作者"""
        return "您的名字"

    def initialize(self, main_window):
        """初始化插件"""
        # 在这里添加初始化代码
        # 可以通过main_window访问主窗口的功能
        # 例如：main_window.tab_widget.addTab(widget, "插件名称")
        pass

    def activate(self):
        """激活插件"""
        # 在这里添加激活代码
        # 例如：切换到插件的选项卡
        pass

    def deactivate(self):
        """停用插件"""
        # 在这里添加停用代码
        # 例如：关闭打开的连接或资源
        pass
```

3. 将插件文件保存到`plugins`目录中，应用程序会在启动时自动加载

### 插件生命周期

1. **加载阶段**：
   - 插件文件被读取
   - 插件类被实例化
   - 插件的`initialize`方法被调用

2. **激活阶段**：
   - 用户选择激活插件
   - 插件的`activate`方法被调用

3. **停用阶段**：
   - 用户选择停用插件或移除插件
   - 插件的`deactivate`方法被调用
   - 插件资源被清理

### 插件最佳实践

1. **资源管理**：
   - 在`initialize`方法中分配资源
   - 在`deactivate`方法中释放资源
   - 确保所有打开的连接和文件都被正确关闭

2. **错误处理**：
   - 在插件方法中添加适当的错误处理
   - 使用`try-except`块捕获异常
   - 通过`main_window.log_message`记录错误信息

3. **用户界面**：
   - 插件界面应该简洁明了
   - 提供清晰的用户反馈
   - 遵循应用程序的整体设计风格

4. **性能考虑**：
   - 避免在插件中进行耗时操作
   - 使用线程处理长时间运行的任务
   - 定期更新插件界面，避免界面冻结

## API 参考

### 主窗口API

插件可以通过`main_window`对象访问以下功能：

#### 属性

- `tab_widget`: QTabWidget，主窗口的选项卡控件
- `plugin_list`: QListWidget，插件列表控件
- `plugin_info`: QTextEdit，插件信息控件
- `log_widget`: QTextEdit，日志输出控件
- `debug_output`: QTextEdit，调试输出控件

#### 方法

- `log_message(message)`: 记录日志消息
  - 参数：message (str) - 日志消息
  - 返回值：无

- `debug_message(message)`: 记录调试消息
  - 参数：message (str) - 调试消息
  - 返回值：无

### 插件接口API

所有插件必须实现以下方法：

- `get_name()`: 返回插件的显示名称
- `get_description()`: 返回插件的功能描述
- `get_version()`: 返回插件的版本号
- `get_author()`: 返回插件的作者信息
- `initialize(main_window)`: 插件初始化，传入主窗口对象
- `activate()`: 激活插件，切换到插件界面
- `deactivate()`: 停用插件，清理资源

### 插件管理器API

插件管理器提供以下方法：

- `load_plugins_from_dir(directory)`: 从目录加载所有插件
- `load_plugin_from_file(file_path)`: 从文件加载插件
- `get_plugin(name)`: 获取插件实例
- `unload_plugin(name)`: 卸载插件
- `get_all_plugins()`: 获取所有插件

## 版本历史

### v1.0.0 (当前版本)

- 初始版本
- 支持插件化架构
- 支持插件动态加载和卸载
- 支持插件持久化
- 支持插件添加和移除功能
- 支持系统插件和用户插件分离

## 许可证

MIT License
