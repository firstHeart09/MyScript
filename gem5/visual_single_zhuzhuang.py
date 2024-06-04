import matplotlib.pyplot as plt
import numpy as np
import ast

def read_txt_to_dict(file_path):
    result_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            # 去除换行符和多余的空格
            line = line.strip()
            if line:
                # 将字符串转化为字典
                line_dict = ast.literal_eval(line)
                # 更新到结果字典中
                result_dict.update(line_dict)
    return result_dict

def autolabel_portrait(rects, ax):
    """
    Attach a text label above each bar in *rects*, displaying its width.
    """
    for rect in rects:
        width = rect.get_width()
        ax.annotate('{}'.format(width),
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center')

# 竖屏显示
def visual_portrait(data):
    """
    data：待显示的数据，默认按照字典处理
    """
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    labels = [keys for keys in data.keys()]  # 保存y轴标签的列表
    data_num_1 = [values[0] for values in data.values()]  # 保存并列的柱状体图中第一列的数据的列表
    data_num_2 = [values[1] for values in data.values()]  # 保存并列的柱状体图中第二列的数据的列表
    
    # 绘制并列柱状图
    y = np.arange(len(labels))  # 标签位置
    height = 0.35  # 条形图的高度，可以根据自己的需求和审美来改

    fig, ax = plt.subplots()
    rects1 = ax.barh(y - height/2, data_num_1, height, label='miss_rate')
    rects2 = ax.barh(y + height/2, data_num_2, height, label='hit_rate')

    # 为x轴、标题和y轴等添加一些文本
    ax.set_xlabel('rate/%', fontsize=16)
    ax.set_ylabel('icache', fontsize=16)
    ax.set_title("ICache's miss and rate")
    ax.set_yticks(y)  # 设置y轴标签
    ax.set_yticklabels(labels)  # 设置标签
    ax.legend()

    # 在rects中的每个条形条上方附加一个文本标签，显示其宽度
    autolabel_portrait(rects1, ax)
    autolabel_portrait(rects2, ax)

    fig.tight_layout()

    plt.savefig('icache.png')  

data = read_txt_to_dict('./different_cacheline.txt')
visual_portrait(data)
