# \method\机器学习（简陋版）\机器学习回归\决策树回归算法.py
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score

def run(data, condition_columns, target_column, test_size=0.2, random_state=42, cross_validation=False, shuffle=False):
    """
    决策树回归器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param test_size: 测试集占比
    :param random_state: 随机种子
    :param cross_validation: 是否进行交叉验证
    :param shuffle: 是否对数据进行洗牌
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    # 数据洗牌
    if shuffle:
        X, y = shuffle_data(X, y, random_state)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # 初始化并训练决策树回归器
    model = DecisionTreeRegressor(random_state=random_state)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # 输出结果
    print(f"决策树回归器的均方误差 (MSE): {mse:.4f}")
    print(f"决策树回归器的R²值: {r2:.4f}")

    # 交叉验证
    if cross_validation:
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
        print(f"交叉验证得分 (负均方误差): {-cv_scores.mean():.4f} (±{cv_scores.std():.4f})")

def shuffle_data(X, y, random_state):
    """洗牌数据"""
    from sklearn.utils import shuffle
    return shuffle(X, y, random_state=random_state)
