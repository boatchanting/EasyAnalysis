import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import os
from datetime import datetime

def run(data, target_column, condition_columns, shuffle=True, train_ratio=0.8, cross_validate=False, 
        random_state=42, export_results=False, output_path=".\\output\\GradientBoosting分类\\{datetime}.txt",
        loss_function='deviance', criterion='friedman_mse', n_estimators=100, learning_rate=0.1, subsample=1.0,
        max_features=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0):
    """
    使用梯度提升树分类算法对数据进行分类，并导出结果到指定文件。
    :param data: 数据源 (Pandas DataFrame)
    :param target_column: 目标列名
    :param condition_columns: 特征列名列表
    :param shuffle: 是否打乱数据
    :param train_ratio: 训练集比例
    :param cross_validate: 是否进行交叉验证
    :param random_state: 随机种子
    :param export_results: 是否导出结果
    :param output_path: 结果输出路径，支持使用 {datetime} 占位符
    :param loss_function: 损失函数
    :param criterion: 节点分裂评价准则
    :param n_estimators: 基学习器数量
    :param learning_rate: 学习率
    :param subsample: 无放回采样比例
    :param max_features: 划分时最大特征比例
    :param min_samples_split: 内部节点分裂的最小样本数
    :param min_samples_leaf: 叶子节点的最小样本数
    :param min_weight_fraction_leaf: 叶子节点中样本的最小权重
    """
    # 检查输入
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了至少一个特征列以及目标列。")
    
    # 数据划分
    X = data[condition_columns]
    y = data[target_column]

    if shuffle:
        data = data.sample(frac=1, random_state=random_state).reset_index(drop=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_ratio, random_state=random_state
    )
    
    # 初始化梯度提升树分类器
    model = GradientBoostingClassifier(
        loss=loss_function,
        criterion=criterion,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        subsample=subsample,
        max_features=max_features,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        min_weight_fraction_leaf=min_weight_fraction_leaf,
        random_state=random_state
    )
    
    if cross_validate:
        scores = cross_val_score(model, X, y, cv=5)
        result = f"交叉验证准确率: {scores.mean():.4f} (标准差: {scores.std():.4f})"
        print(result)
    else:
        # 模型训练
        model.fit(X_train, y_train)
        
        # 预测与评估
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        result = f"梯度提升树分类器的准确率: {acc:.4f}\n分类报告:\n{report}"
        print(result)
    
    # 如果需要导出结果
    if export_results:
        # 替换路径中的 {datetime} 占位符
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_path.format(datetime=current_datetime)

        # 创建目录（如果不存在）
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 将结果保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"结果已导出至: {output_file}")
