#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口类
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QMenu, QAction, QToolBar,
                            QStatusBar, QTabWidget, QVBoxLayout, QWidget,
                            QMessageBox, QFileDialog, QDockWidget, QTextEdit,
                            QListWidget, QListWidgetItem, QSplitter, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QTextCursor

# 根据运行方式选择导入方式
try:
    from .plugin_manager import PluginManager
    from .plugin_interface import PluginInterface
except ImportError:
    from plugin_manager import PluginManager
    from plugin_interface import PluginInterface


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.loaded_plugins = {}
        self.init_ui()
        self.load_plugins()

    def init_ui(self):
        """初始化UI"""
        # 创建菜单栏
        self.create_menu_bar()

        # 创建工具栏
        self.create_toolbar()

        # 创建状态栏
        self.statusBar().showMessage("就绪")

        # 创建中央部件
        self.create_central_widget()

        # 创建插件管理面板
        self.create_plugin_panel()

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        # 退出动作
        exit_action = QAction("退出(&E)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("退出应用程序")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 插件菜单
        self.plugin_menu = menubar.addMenu("插件(&P)")

        # 加载插件动作
        load_plugin_action = QAction("加载插件(&L)...", self)
        load_plugin_action.setShortcut("Ctrl+L")
        load_plugin_action.setStatusTip("加载一个新插件")
        load_plugin_action.triggered.connect(self.load_plugin_from_file)
        self.plugin_menu.addAction(load_plugin_action)

        self.plugin_menu.addSeparator()

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")

        # 关于动作
        about_action = QAction("关于(&A)", self)
        about_action.setStatusTip("关于此应用程序")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("主工具栏")
        # 工具栏暂时为空，可根据需要添加其他常用功能按钮

    def create_central_widget(self):
        """创建中央部件"""
        # 创建主分割器
        self.main_splitter = QSplitter(Qt.Horizontal)

        # 创建日志窗口
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setPlaceholderText("日志输出将显示在这里...")

        # 创建调试输出窗口
        self.debug_output = QTextEdit()
        self.debug_output.setReadOnly(True)
        self.debug_output.setPlaceholderText("调试输出将显示在这里...")

        # 创建选项卡
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.debug_output, "调试输出")
        self.tab_widget.addTab(self.log_widget, "日志")

        # 将选项卡添加到分割器
        self.main_splitter.addWidget(self.tab_widget)

        # 设置分割器比例
        self.main_splitter.setStretchFactor(0, 2)

        # 设置中央部件
        self.setCentralWidget(self.main_splitter)

    def create_plugin_panel(self):
        """创建插件面板"""
        # 创建插件列表
        self.plugin_list = QListWidget()
        self.plugin_list.itemClicked.connect(self.on_plugin_selected)

        # 创建插件信息面板
        self.plugin_info = QTextEdit()
        self.plugin_info.setReadOnly(True)
        self.plugin_info.setPlaceholderText("插件信息将显示在这里...")
        self.plugin_info.setMaximumHeight(150)

        # 创建移除插件按钮
        self.remove_plugin_button = QPushButton("移除插件")
        self.remove_plugin_button.clicked.connect(self.remove_selected_plugin)
        self.remove_plugin_button.setEnabled(False)  # 初始状态为禁用

        # 创建按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addWidget(self.remove_plugin_button)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # 创建插件面板分割器
        plugin_splitter = QSplitter(Qt.Vertical)
        plugin_splitter.addWidget(self.plugin_list)
        plugin_splitter.addWidget(button_container)
        plugin_splitter.addWidget(self.plugin_info)

        # 创建插件面板Dock
        plugin_dock = QDockWidget("插件管理", self)
        plugin_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        plugin_dock.setWidget(plugin_splitter)

        # 添加到主窗口（左侧）
        self.addDockWidget(Qt.LeftDockWidgetArea, plugin_dock)

    def load_plugins(self):
        """加载所有插件（系统插件和用户插件）"""
        # 重定向标准输出，以便捕获print语句
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            # 加载所有插件
            plugins = self.plugin_manager.load_all_plugins()

        # 将捕获的输出显示在日志窗口中
        captured_output = output.getvalue()
        if captured_output:
            self.log_message(f"插件加载输出:\n{captured_output}")

        # 添加到插件列表
        for plugin_name, plugin in plugins.items():
            self.add_plugin_to_list(plugin_name, plugin)

        self.log_message(f"加载了 {len(plugins)} 个插件")
        self.log_message(f"系统插件目录: {self.plugin_manager.system_plugin_dir}")
        self.log_message(f"用户插件目录: {self.plugin_manager.user_plugin_dir}")

    def load_plugin_from_file(self):
        """从文件加载插件"""
        # 获取用户主目录作为默认路径
        home_dir = os.path.expanduser("~")

        # 打开文件选择对话框，默认路径为用户主目录
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择插件文件", home_dir, "Python 文件 (*.py);;所有文件 (*)"
        )

        if not file_path:
            return

        # 使用用户插件目录
        plugins_dir = self.plugin_manager.user_plugin_dir

        # 获取插件文件名
        plugin_filename = os.path.basename(file_path)
        plugin_name = plugin_filename.split('.')[0]

        # 目标文件路径
        target_path = os.path.join(plugins_dir, plugin_filename)

        # 检查插件是否已存在
        if os.path.exists(target_path) and plugin_name in self.loaded_plugins:
            reply = QMessageBox.question(
                self,
                "插件已存在",
                f"插件 '{plugin_name}' 已存在，是否要替换？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                self.log_message(f"取消加载插件: {plugin_name}")
                return
            # 移除旧插件
            self.remove_plugin(plugin_name)

        # 复制插件文件到用户插件目录
        try:
            import shutil
            shutil.copy2(file_path, target_path)
            self.log_message(f"插件文件已复制到: {target_path}")
        except Exception as e:
            QMessageBox.critical(self, "复制插件文件失败", f"无法复制插件文件:\n{str(e)}")
            return

        # 加载插件
        try:
            # 重定向标准输出，以便捕获print语句
            import io
            from contextlib import redirect_stdout

            output = io.StringIO()
            with redirect_stdout(output):
                plugin = self.plugin_manager.load_plugin_from_file(target_path)

            # 将捕获的输出显示在日志窗口中
            captured_output = output.getvalue()
            if captured_output:
                self.log_message(f"插件加载输出:\n{captured_output}")

            if plugin:
                self.add_plugin_to_list(plugin_name, plugin)
                self.log_message(f"成功加载插件: {plugin_name}")
            else:
                error_msg = "无法加载插件，请检查插件是否实现了正确的接口。"
                self.log_message(f"加载插件失败: {error_msg}")
                QMessageBox.warning(self, "加载插件失败", error_msg)
        except Exception as e:
            error_msg = f"加载插件时发生错误:\n{str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, "加载插件错误", error_msg)

    def add_plugin_to_list(self, name, plugin):
        """添加插件到列表"""
        # 使用插件自己提供的名称
        display_name = plugin.get_name()

        # 创建列表项
        item = QListWidgetItem(display_name)
        item.setData(Qt.UserRole, plugin)

        # 添加到列表
        self.plugin_list.addItem(item)

        # 添加到已加载插件字典
        self.loaded_plugins[name] = plugin

        # 创建插件菜单项
        plugin_action = QAction(display_name, self)
        plugin_action.triggered.connect(lambda checked, p=plugin: p.activate())
        self.plugin_menu.addAction(plugin_action)

        # 初始化插件
        try:
            plugin.initialize(self)
        except Exception as e:
            self.log_message(f"初始化插件 {name} 失败: {str(e)}")

    def remove_plugin(self, name):
        """移除插件"""
        if name not in self.loaded_plugins:
            return

        plugin = self.loaded_plugins[name]
        display_name = plugin.get_name()

        # 停用插件
        try:
            plugin.deactivate()
        except Exception as e:
            self.log_message(f"停用插件 {name} 失败: {str(e)}")

        # 从插件列表中移除
        for i in range(self.plugin_list.count()):
            item = self.plugin_list.item(i)
            if item and item.data(Qt.UserRole) == plugin:
                self.plugin_list.takeItem(i)
                break

        # 从菜单中移除
        for action in self.plugin_menu.actions():
            if action.text() == display_name:
                self.plugin_menu.removeAction(action)
                break

        # 从选项卡中移除（如果插件创建了选项卡）
        if hasattr(plugin, 'serial_widget'):
            index = self.tab_widget.indexOf(plugin.serial_widget)
            if index >= 0:
                self.tab_widget.removeTab(index)

        # 从已加载插件字典中移除
        del self.loaded_plugins[name]

        self.log_message(f"已移除插件: {name}")

    def on_plugin_selected(self, item):
        """插件选择事件处理"""
        plugin = item.data(Qt.UserRole)

        # 显示插件信息
        info = f"插件名称: {item.text()}\n"
        info += f"插件描述: {plugin.get_description()}\n"
        info += f"插件版本: {plugin.get_version()}\n"
        info += f"插件作者: {plugin.get_author()}\n"

        self.plugin_info.setText(info)

        # 启用移除插件按钮
        self.remove_plugin_button.setEnabled(True)

    def remove_selected_plugin(self):
        """移除选中的插件"""
        # 获取当前选中的项
        current_item = self.plugin_list.currentItem()

        if not current_item:
            return

        # 获取插件实例
        plugin = current_item.data(Qt.UserRole)

        # 查找插件名称
        plugin_name = None
        for name, loaded_plugin in self.loaded_plugins.items():
            if loaded_plugin == plugin:
                plugin_name = name
                break

        if not plugin_name:
            self.log_message("无法确定插件名称")
            return

        # 确认是否移除插件
        reply = QMessageBox.question(
            self,
            "确认移除",
            f"确定要移除插件 '{plugin.get_name()}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # 移除插件文件（从用户目录或系统目录）
        try:
            # 先尝试从用户目录删除
            plugin_file = os.path.join(self.plugin_manager.user_plugin_dir, f"{plugin_name}.py")

            if not os.path.exists(plugin_file):
                # 如果用户目录不存在，尝试从系统目录删除
                plugin_file = os.path.join(self.plugin_manager.system_plugin_dir, f"{plugin_name}.py")

            if os.path.exists(plugin_file):
                os.remove(plugin_file)
                self.log_message(f"已删除插件文件: {plugin_file}")
            else:
                self.log_message(f"未找到插件文件: {plugin_file}")
        except Exception as e:
            self.log_message(f"删除插件文件失败: {str(e)}")

        # 移除插件
        self.remove_plugin(plugin_name)

        # 禁用移除插件按钮
        self.remove_plugin_button.setEnabled(False)

    def log_message(self, message):
        """记录日志消息"""
        self.log_widget.append(message)

        # 自动滚动到底部
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_widget.setTextCursor(cursor)

    def debug_message(self, message):
        """记录调试消息"""
        self.debug_output.append(message)

        # 自动滚动到底部
        cursor = self.debug_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.debug_output.setTextCursor(cursor)

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于",
                         "可添加插件的调试助手\n\n"
                         "一个支持动态加载插件的调试工具，"
                         "可以通过添加插件来扩展功能。\n\n"
                         "版本: 1.0.0")
