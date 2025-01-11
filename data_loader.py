# main.py

import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QGuiApplication

# 从 DL 包中导入函数
from DL import (init_ui,load_stylesheet,detect_encoding,load_data,drag_enter_event,drop_event,set_window_size)

class DataLoader(QWidget):
    # 定义信号
    data_loaded = pyqtSignal(pd.DataFrame)  # 信号：数据加载完成，传递 Pandas DataFrame

    def __init__(self):
        super().__init__()
        init_ui(self)
        self.set_window_size()

    # 在类中绑定从模块导入的函数
    load_stylesheet = load_stylesheet
    detect_encoding = detect_encoding
    load_data = load_data
    dragEnterEvent = drag_enter_event
    dropEvent = drop_event
    set_window_size = set_window_size

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = DataLoader()
    window.show()
    sys.exit(app.exec_())
