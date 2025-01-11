# DA/run_analysis.py

import io,os,sys,json
import importlib
from PyQt5.QtWidgets import QComboBox, QLineEdit, QSpinBox, QCheckBox, QListWidget, QPushButton
from PyQt5.QtGui import QDoubleValidator, QIntValidator

class TextCapture(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        super().write(message)
        # 每次捕获到输出信息时，更新到 QTextEdit 中
        self.text_widget.append(message)  # 使用 append 来追加文本

def run_analysis(self):
    """
    执行选中的算法
    """
    if not self.current_algorithm:
        self.status_label.setText("请先选择算法")
        return

    # 获取当前选中的算法配置文件路径
    algorithm_json_path = self.current_algorithm
    algorithm_dir = os.path.dirname(algorithm_json_path)
    
    # 读取 JSON 配置文件
    try:
        with open(algorithm_json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        self.status_label.setText(f"读取配置文件失败：{e}")
        return
    
    # 获取算法脚本路径 (脚本与配置文件同名，只是扩展名不同)
    algorithm_script_path = os.path.join(algorithm_dir, config['algorithm'] + '.py')
    
    # 确保脚本文件存在
    if not os.path.exists(algorithm_script_path):
        self.status_label.setText(f"算法脚本 {algorithm_script_path} 不存在")
        return

    # 收集用户输入的参数，并映射到 run 函数的参数名称
    params = {}
    output_widget = None
    for param in config["parameters"]:
        param_name = param["name"]
        param_function = param["function"]  # 从配置文件获取函数名
        widget = self.parameter_widgets.get(param_name)

        if widget:
            if isinstance(widget, QComboBox):
                params[param_function] = widget.currentText()
            elif isinstance(widget, QLineEdit):
                if isinstance(widget.validator(), QDoubleValidator):
                    try:
                        params[param_function] = float(widget.text())
                    except ValueError:
                        self.status_label.setText(f"{param['name']} 输入无效")
                        return
                elif isinstance(widget.validator(), QIntValidator):
                    try:
                        params[param_function] = int(widget.text())
                    except ValueError:
                        self.status_label.setText(f"{param['name']} 输入无效")
                        return
            elif isinstance(widget, QSpinBox):
                params[param_function] = widget.value()
            elif isinstance(widget, QCheckBox):
                params[param_function] = widget.isChecked()
            elif isinstance(widget, QListWidget):
                params[param_function] = [item.text() for item in widget.selectedItems()]
            elif isinstance(widget, QPushButton):
                params[param_function] = widget.property("selected_color") or param.get('default', '#FFFFFF')

    # 创建一个用于捕获 print 输出的 TextCapture 实例，并重定向标准输出
    if output_widget:
        capture = TextCapture(output_widget)
        sys.stdout = capture  # 重定向标准输出

    # 动态加载算法脚本
    try:
        spec = importlib.util.spec_from_file_location(config['algorithm'], algorithm_script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 调用算法的 run 函数并传递参数
        module.run(self.data, **params)
        self.status_label.setText(f"算法 {config['algorithm']} 执行成功")
    except Exception as e:
        self.status_label.setText(f"算法执行失败：{e}")
    finally:
        sys.stdout = sys.__stdout__

