# 插件目录

此目录用于存放系统插件。

## 插件开发

插件需要继承`PluginInterface`类并实现以下方法：

- `get_name()`: 返回插件名称
- `get_description()`: 返回插件描述
- `get_version()`: 返回插件版本
- `get_author()`: 返回插件作者

可选实现的方法：

- `initialize(main_window)`: 初始化插件
- `activate()`: 激活插件
- `deactivate()`: 停用插件

## 插件导入

插件文件中必须使用以下方式导入PluginInterface：

```python
from debug_assistant.plugin_interface import PluginInterface
```

不要使用相对导入或直接导入plugin_interface，这会导致加载失败。

## 插件目录

- 系统插件目录：`/usr/lib/debug-assistant/plugins/`（需要root权限）
- 用户插件目录：`~/.local/share/debug-assistant/plugins/`（无需root权限）

详见PLUGIN_PERMISSIONS.md了解插件权限管理机制
