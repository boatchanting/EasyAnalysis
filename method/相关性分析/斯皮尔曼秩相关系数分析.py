# \method\相关性分析\斯皮尔曼秩相关系数分析.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

def run(data, condition_columns, target_column, visualize=False, chart_title="Spearman Correlation Heatmap"):
    """
    斯皮尔曼秩相关系数分析
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param visualize: 是否启用可视化
    :param chart_title: 可视化图表的标题
    """
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")

    # 计算斯皮尔曼相关系数
    spearman_corr, _ = spearmanr(data[condition_columns + [target_column]])

    # 输出斯皮尔曼相关系数
    print("斯皮尔曼相关系数矩阵:")
    corr_df = pd.DataFrame(spearman_corr, index=condition_columns + [target_column], columns=condition_columns + [target_column])
    print(corr_df)

    # 可视化
    if visualize:
        plt.figure(figsize=(10, 8))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title(chart_title)
        plt.show()
