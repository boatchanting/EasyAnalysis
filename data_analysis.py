# data_analysis.py

import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QHBoxLayout, QComboBox, QLineEdit, QListWidget, QCheckBox, QColorDialog, QSpinBox, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import importlib
# 导入 数据分析模块 包中的函数
from DA import load_algorithm_parameters, run_analysis, init_ui, load_algorithms, find_tree_item, select_color, update_columns, clear_layout,load_stylesheet

class DataAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        init_ui(self)
        self.data = None  # 用于存储当前加载的数据
        self.current_algorithm = None
        self.current_parameters = {}
        self.parameter_widgets = {}  # 保存参数控件，方便获取值

    # 在类中绑定由模块导入的函数
    load_stylesheet = load_stylesheet    

    def update_columns(self, data):
        """
        更新数据列名，在参数界面需要时使用
        :param data: 当前加载的数据 (Pandas DataFrame)
        """
        update_columns(self, data)

    def load_algorithms(self):
        """
        加载 method/ 目录下的 JSON 配置文件，并构建树状结构
        """
        load_algorithms(self)

    def find_tree_item(self, path):
        """
        根据相对路径在树中查找对应的 QTreeWidgetItem
        """
        return find_tree_item(self, path)

    def on_algorithm_selected(self, item, column):
        """
        当用户在树中选择算法时，更新参数设置界面
        """
        algorithm_path = item.data(0, Qt.UserRole)
        if algorithm_path and algorithm_path.endswith('.json'):
            self.current_algorithm = os.path.join('method', algorithm_path)
            load_algorithm_parameters(self)

    def run_analysis(self):
        """
        执行选中的算法
        """
        run_analysis(self)

    def select_color(self):
        """
        用于打开颜色选择器和储存颜色配置参数
        """
        select_color(self)

    @staticmethod
    def clear_layout(layout):
        """
        清除布局中的所有控件
        """
        clear_layout(layout)
