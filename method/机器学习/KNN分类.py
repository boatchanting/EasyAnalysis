# \method\KNN分类.py
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import numpy as np

def run(data, condition_columns, target_column, n_neighbors=5, algorithm="auto", p=2, metric="minkowski", visualize=False, random_state=42):
    """
    KNN分类器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param n_neighbors: KNN中的邻居数
    :param algorithm: 用于计算距离的算法
    :param p: 距离度量参数（默认为欧几里得距离）
    :param metric: 距离度量方式
    :param visualize: 是否进行分类结果的可视化
    :param random_state: 随机种子
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练KNN分类器
    model = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=algorithm, p=p, metric=metric)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # 输出结果
    print(f"KNN分类器的准确率: {acc:.4f}")
    print("分类报告:")
    print(report)
    
    # 可视化分类结果
    if visualize:
        # 可视化数据点和分类中心
        plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_pred, cmap='viridis', s=50)
        centers = np.array([model.transform(X_test.iloc[:, :2]).mean(axis=0)])  # 求平均值作为中心
        plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='red', s=100)
        plt.title("KNN 分类结果可视化")
        plt.xlabel("特征1")
        plt.ylabel("特征2")
        plt.show()
