# \method\机器学习\机器学习分类\KNN分类.py
import os
import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

def intcv(cv):
    """
    将交叉验证折数转换为整数
    :param cv: 交叉验证折数
    :return: 整数形式的交叉验证折数
    """
    if cv == "None":
        cv = None
    else:
        cv = int(cv)

def run(data, 
        condition_columns, 
        target_column, 
        n_neighbors=5, 
        metric='euclidean', 
        algorithm='auto', 
        shuffle=False, 
        train_size=0.8, 
        cv=None, 
        export_centers=False, 
        output_path='./output/KNN分类/', 
        visualize=False, 
        chart_title="KNN分类"):
    """
    KNN分类
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 特征列名列表
    :param target_column: 目标列名
    :param n_neighbors: 近邻数 (默认为5)
    :param metric: 距离度量方式 (默认为欧氏距离)
    :param algorithm: 搜索算法 (默认为auto)
    :param shuffle: 是否进行数据洗牌 (默认为False)
    :param train_size: 训练集占比 (默认为0.8)
    :param cv: 交叉验证折数 (默认为无)
    :param export_centers: 是否导出分类中心结果 (默认为False)
    :param output_path: 导出路径 (默认为'./output/KNN分类/')
    :param visualize: 是否可视化 (默认为False)
    :param chart_title: 可视化图表名称 (默认为"KNN分类")
    """
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")

    # 数据预处理
    X = data[condition_columns]
    y = data[target_column]
    if shuffle:
        data = data.sample(frac=1).reset_index(drop=True)

    # 数据划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=42)

    # 初始化分类器
    knn = KNeighborsClassifier(n_neighbors=n_neighbors, metric=metric, algorithm=algorithm)

    # 如果指定了交叉验证
    cv=intcv(cv)
    if cv:
        scores = cross_val_score(knn, X, y, cv=cv)
        print(f"交叉验证平均得分: {np.mean(scores):.2f}")

    # 训练模型
    knn.fit(X_train, y_train)

    # 测试集评估
    accuracy = knn.score(X_test, y_test)
    print(f"测试集准确率: {accuracy:.2f}")

    # 是否导出分类中心
    if export_centers:
        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(output_file, 'w',encoding='utf-8') as f:
            f.write(f"分类器参数:\n邻居数: {n_neighbors}\n距离度量: {metric}\n算法: {algorithm}\n\n测试集准确率: {accuracy:.2f}\n")
        print(f"分类中心结果已导出至: {output_file}")

    # 可视化
    if visualize:
        plt.figure(figsize=(8, 6))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        for class_value in np.unique(y):
            plt.scatter(X.loc[y == class_value, condition_columns[0]], 
                        X.loc[y == class_value, condition_columns[1]], 
                        label=f"类别 {class_value}")
        plt.title(chart_title)
        plt.xlabel(condition_columns[0])
        plt.ylabel(condition_columns[1])
        plt.legend()
        plt.show()
