#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件接口定义
"""

from abc import ABC, abstractmethod


class PluginInterface(ABC):
    """插件接口基类"""

    @abstractmethod
    def get_name(self):
        """获取插件名称"""
        pass

    @abstractmethod
    def get_description(self):
        """获取插件描述"""
        pass

    @abstractmethod
    def get_version(self):
        """获取插件版本"""
        pass

    @abstractmethod
    def get_author(self):
        """获取插件作者"""
        pass

    def initialize(self, main_window):
        """初始化插件

        Args:
            main_window: 主窗口实例，插件可以通过它访问主窗口的功能
        """
        pass

    def activate(self):
        """激活插件"""
        pass

    def deactivate(self):
        """停用插件"""
        pass
