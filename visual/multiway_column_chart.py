import matplotlib.pyplot as plt
import numpy as np

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

def visual_portrait():
    """
    data：待显示的数据，默认按照字典处理
    output_dir：要保存的可视化的文件路径
    """
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']  # 保存y轴标签的列表
    data_num_1 = [20, 34, 30, 35, 27]  # 保存并列的柱状体图中第一列的数据的列表
    data_num_2 = [25, 32, 34, 20, 25]  # 保存并列的柱状体图中第二列的数据的列表
    
    # 绘制并列柱状图
    y = np.arange(len(labels))  # 标签位置
    height = 0.35  # 条形图的高度，可以根据自己的需求和审美来改

    fig, ax = plt.subplots()
    rects1 = ax.barh(y - height/2, data_num_1, height, label='柱1标志')
    rects2 = ax.barh(y + height/2, data_num_2, height, label='柱2标志')

    # 为x轴、标题和y轴等添加一些文本
    ax.set_xlabel('X轴', fontsize=16)
    ax.set_ylabel('Y轴', fontsize=16)
    ax.set_title('这里是标题')
    ax.set_yticks(y)  # 设置y轴标签
    ax.set_yticklabels(labels)  # 设置标签
    ax.legend()

    # 在rects中的每个条形条上方附加一个文本标签，显示其宽度
    autolabel_portrait(rects1, ax)
    autolabel_portrait(rects2, ax)

    fig.tight_layout()

    plt.show()


def autolabel_landscape(rects, ax):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def visual_landscape():
    """
    data：待显示的数据，默认按照字典处理
    output_dir：要保存的可视化的文件路径
    """
    # plt.rcParams['font.sans-serif']=['Arial']  # 解决中文乱码
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']  # 保存x轴标签的列表
    data_num_1 = [20, 34, 30, 35, 27]  # 保存并列的柱状体图中第一列的数据的列表
    data_num_2 = [25, 32, 34, 20, 25]  # 保存并列的柱状体图中第二列的数据的列表
    
    # 绘制并列柱状图
    x = np.arange(len(labels))  # 标签位置
    width = 0.35  # 柱状图的宽度，可以根据自己的需求和审美来改

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, data_num_1, width, label='data_num_1')
    rects2 = ax.bar(x + width/2, data_num_2, width, label='data_num_2')

    # 为y轴、标题和x轴等添加一些文本
    ax.set_ylabel('Y轴', fontsize=16)
    ax.set_xlabel('X轴', fontsize=16)
    ax.set_title('这里是标题')
    ax.set_xticks(x)  # 设置x轴标签
    ax.set_xticklabels(labels)  # 设置标签
    ax.legend()

    # 在rects中的每个柱状条上方附加一个文本标签，显示其高度
    autolabel_landscape(rects1, ax)
    autolabel_landscape(rects2, ax)

    fig.tight_layout()

    plt.show()

visual_landscape()
visual_portrait()
