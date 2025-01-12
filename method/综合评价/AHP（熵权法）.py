# \method\综合评价\AHP（熵权法）.py
import os
import numpy as np
import pandas as pd

def run(data, positive_columns, negative_columns, output_weights=False, output_path="./output/AHP/weights.txt"):
    """
    AHP（熵权法）算法实现
    :param data: 数据源 (Pandas DataFrame)
    :param positive_columns: 选择的正向指标列名列表
    :param negative_columns: 选择的负向指标列名列表
    :param output_weights: 是否输出权重文件 (布尔值)
    :param output_path: 权重文件输出路径 (字符串)
    :return: 各指标的熵权
    """
    # 检查列是否满足条件
    if len(positive_columns) + len(negative_columns) < 2:
        raise ValueError("正向指标加负向指标数目必须大于等于2")

    # 数据预处理
    selected_columns = positive_columns + negative_columns
    if not all(col in data.columns for col in selected_columns):
        raise ValueError("选择的列名必须存在于数据中")

    # 数据归一化
    normalized_data = data[selected_columns].copy()
    for col in positive_columns:
        normalized_data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
    for col in negative_columns:
        normalized_data[col] = (data[col].max() - data[col]) / (data[col].max() - data[col].min())

    # 计算每列的熵值
    P = normalized_data / normalized_data.sum(axis=0)
    entropy = -np.nansum(P * np.log(P + 1e-12), axis=0) / np.log(len(data))
    weights = (1 - entropy) / (1 - entropy).sum()

    # 打印权重
    print("指标权重：")
    for col, weight in zip(selected_columns, weights):
        print(f"{col}: {weight:.4f}")

    # 输出权重文件
    if output_weights:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("指标权重：\n")
            for col, weight in zip(selected_columns, weights):
                f.write(f"{col}: {weight:.4f}\n")
            print(f"权重文件已保存至: {output_path}")


    return dict(zip(selected_columns, weights))
