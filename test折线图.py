import importlib.util
import pandas as pd

# 1. 加载脚本文件
def load_script(script_path):
    spec = importlib.util.spec_from_file_location("line_chart_algorithm", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 2. 主程序：执行折线图算法
def execute_line_chart(data, column, color="#0000FF", linestyle="-", title="折线图"):
    # 加载折线图算法脚本
    script_path = "method\绘图\折线图（1列）.py"  # 假设脚本和主程序在同一个目录下
    algorithm_module = load_script(script_path)
    
    # 调用折线图绘制函数
    algorithm_module.plot_line_chart(data, column, color, linestyle, title)

# 3. 示例数据
data = pd.DataFrame({
    "销量": [100, 200, 150, 300, 250, 400],
    "日期": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"]
})

# 4. 执行折线图绘制
execute_line_chart(data, column="销量", color="#FF6347", linestyle="--", title="2023年销量折线图")
