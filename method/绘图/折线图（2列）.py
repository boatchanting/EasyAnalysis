import matplotlib.pyplot as plt

def run(data, col1, col2, line1_color="a4133c", line2_color='ff4d6d', line1_style='-', line2_style='-', use_two_axes=False, fill_between_lines=True, chart_title="折线图（2列）",font_size=16):
    """
    生成折线图（2列）
    :param data: 数据源 (Pandas DataFrame)
    :param col1: 第一类定量变量的列名
    :param col2: 第二类定量变量的列名
    :param line1_color: 折线1的颜色 (默认 'a4133c')
    :param line2_color: 折线2的颜色 (默认 'ff4d6d')
    :param line1_style: 折线1的线型 (默认 '-')
    :param line2_style: 折线2的线型 (默认 '-')
    :param use_two_axes: 是否使用两个坐标轴 (默认 False, 使用1个坐标轴)
    :param fill_between_lines: 是否将两折线间区域用灰色填充 (默认 True, 填充)
    :param chart_title: 可视化图表的标题 (默认 '折线图（2列）')
    :param font_size: 字体大小 (默认 16)
    """
    # 检查数据列是否存在
    if col1 not in data.columns or col2 not in data.columns:
        raise ValueError(f"数据中未找到列 {col1} 或 {col2}")

    # 创建画布
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 设置字体大小
    plt.rcParams['font.size'] = font_size
    # 绘制第一条折线
    ax1.plot(data[col1], color=line1_color, linestyle=line1_style, label=col1)
    ax1.set_xlabel('样本')
    ax1.set_ylabel(col1, color=line1_color)
    ax1.tick_params(axis='y', labelcolor=line1_color)
    
    if use_two_axes:
        # 如果使用两个坐标轴，则创建第二个坐标轴
        ax2 = ax1.twinx()
        ax2.plot(data[col2], color=line2_color, linestyle=line2_style, label=col2)
        ax2.set_ylabel(col2, color=line2_color)
        ax2.tick_params(axis='y', labelcolor=line2_color)
    else:
        # 单个坐标轴绘制第二条折线
        ax1.plot(data[col2], color=line2_color, linestyle=line2_style, label=col2)
    
    # 填充折线间的区域
    if fill_between_lines:
        ax1.fill_between(data.index, data[col1], data[col2], color='gray', alpha=0.3)
    
    # 设置图表标题
    plt.title(chart_title)
    
    # 展示图例
    ax1.legend(loc='upper left')
    
    # 显示图表
    plt.tight_layout()
    plt.show()

