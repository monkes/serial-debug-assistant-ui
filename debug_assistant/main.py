#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可添加插件的调试助手 - 主程序入口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QPluginLoader, QObject
from PyQt5.QtGui import QIcon

# 根据运行方式选择导入方式
try:
    from .main_window import MainWindow
except ImportError:
    from main_window import MainWindow


def main():
    # 创建应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("调试助手")
    app.setOrganizationName("Debug Assistant")
    app.setApplicationDisplayName("调试助手")

    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "icon256x256.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 创建主窗口
    window = MainWindow()
    window.setWindowTitle("调试助手")
    window.setObjectName("调试助手")
    window.resize(1200, 800)
    window.show()

    # 运行应用
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
