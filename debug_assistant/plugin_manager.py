#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件管理器
"""

import os
import sys
import importlib.util

# 根据运行方式选择导入方式
try:
    from .plugin_interface import PluginInterface
except ImportError:
    from plugin_interface import PluginInterface


class PluginManager:
    """插件管理器类"""

    def __init__(self):
        """初始化插件管理器"""
        self.plugins = {}
        # 系统插件目录
        # 如果在开发环境中运行，使用项目目录中的插件目录
        # 否则使用安装后的插件目录
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')):
            self.system_plugin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')
        else:
            self.system_plugin_dir = '/usr/lib/debug-assistant/plugins'
        # 用户插件目录
        self.user_plugin_dir = os.path.expanduser('~/.local/share/debug-assistant/plugins')

        # 确保用户插件目录存在
        os.makedirs(self.user_plugin_dir, exist_ok=True)

    def load_all_plugins(self):
        """加载所有插件（系统插件和用户插件）

        Returns:
            dict: 加载的插件字典 {plugin_name: plugin_instance}
        """
        all_plugins = {}

        # 先加载系统插件
        system_plugins = self.load_plugins_from_dir(self.system_plugin_dir)
        all_plugins.update(system_plugins)

        # 再加载用户插件（会覆盖同名的系统插件）
        user_plugins = self.load_plugins_from_dir(self.user_plugin_dir)
        all_plugins.update(user_plugins)

        return all_plugins

    def load_plugins_from_dir(self, directory):
        """从目录加载所有插件

        Args:
            directory: 插件目录路径

        Returns:
            dict: 加载的插件字典 {plugin_name: plugin_instance}
        """
        plugins = {}

        # 如果目录不存在，返回空字典
        if not os.path.exists(directory):
            return plugins

        # 遍历目录中的所有Python文件
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                file_path = os.path.join(directory, filename)

                try:
                    plugin = self.load_plugin_from_file(file_path)
                    if plugin:
                        plugin_name = os.path.basename(file_path).split('.')[0]
                        plugins[plugin_name] = plugin
                except Exception as e:
                    print(f"加载插件 {filename} 失败: {str(e)}")

        return plugins

    def load_plugin_from_file(self, file_path):
        """从文件加载插件

        Args:
            file_path: 插件文件路径

        Returns:
            PluginInterface: 插件实例，如果加载失败则返回None
        """
        # 获取插件名称
        plugin_name = os.path.basename(file_path).split('.')[0]

        # 如果插件已经加载，则返回已加载的插件
        if plugin_name in self.plugins:
            return self.plugins[plugin_name]

        try:
            # 确保debug_assistant包的路径在sys.path中
            debug_assistant_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if debug_assistant_path not in sys.path:
                sys.path.insert(0, debug_assistant_path)

            # 动态导入插件模块
            spec = importlib.util.spec_from_file_location(plugin_name, file_path)
            if spec is None or spec.loader is None:
                print(f"无法创建模块规范: {file_path}")
                return None

            module = importlib.util.module_from_spec(spec)
            # 使用唯一的模块名，避免冲突
            unique_module_name = f"debug_assistant_plugin_{plugin_name}"
            sys.modules[unique_module_name] = module

            # 创建一个虚拟的plugin_interface模块，包含PluginInterface
            # 这样插件可以使用"from plugin_interface import PluginInterface"导入
            plugin_interface_module = type('module', (), {'PluginInterface': PluginInterface})()
            sys.modules['plugin_interface'] = plugin_interface_module

            # 执行模块
            spec.loader.exec_module(module)

            # 查找插件类
            plugin_class = None
            for attr_name in dir(module):
                try:
                    attr = getattr(module, attr_name)

                    # 检查是否是类
                    if not isinstance(attr, type):
                        continue

                    # 检查是否是插件接口的子类且不是接口本身
                    try:
                        if attr is PluginInterface:
                            continue
                        if issubclass(attr, PluginInterface):
                            plugin_class = attr
                            break
                    except TypeError:
                        # 如果issubclass失败，继续检查下一个属性
                        continue
                except Exception as e:
                    print(f"检查属性 {attr_name} 时出错: {str(e)}")
                    continue

            if plugin_class is None:
                print(f"未找到插件类: {file_path}")
                # 打印模块中的所有类，帮助调试
                print(f"模块 {plugin_name} 中的类:")
                for attr_name in dir(module):
                    try:
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type):
                            print(f"  - {attr_name}: {attr}")
                    except:
                        pass
                return None

            # 创建插件实例
            plugin_instance = plugin_class()

            # 添加到插件字典
            self.plugins[plugin_name] = plugin_instance

            return plugin_instance

        except ImportError as e:
            print(f"导入插件 {file_path} 失败（导入错误）: {str(e)}")
            return None
        except AttributeError as e:
            print(f"导入插件 {file_path} 失败（属性错误）: {str(e)}")
            return None
        except Exception as e:
            print(f"加载插件 {file_path} 失败（未知错误）: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def get_plugin(self, name):
        """获取插件实例

        Args:
            name: 插件名称

        Returns:
            PluginInterface: 插件实例，如果插件不存在则返回None
        """
        return self.plugins.get(name)

    def unload_plugin(self, name):
        """卸载插件

        Args:
            name: 插件名称

        Returns:
            bool: 是否成功卸载
        """
        if name in self.plugins:
            plugin = self.plugins[name]
            plugin.deactivate()
            del self.plugins[name]
            return True
        return False

    def get_all_plugins(self):
        """获取所有插件

        Returns:
            dict: 所有插件字典 {plugin_name: plugin_instance}
        """
        return self.plugins
