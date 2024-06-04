import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import argparse
 
def my_args():
    """
    自定义运行此脚本传入的参数
    """
    parser = argparse.ArgumentParser(description='Extract debugging information from gem5')
    parser.add_argument("--path", default="1", type=str, nargs ='?', required=True,
                        help=f"path")
    parser.add_argument("--name", default="2", type=str, nargs ='?', required=True,
                        help=f"png name")

    options = parser.parse_args()
    return options


def read_from_file(filename):
    data = []
    with open(filename, 'r') as f_in:
        lines = f_in.readlines()
        for line in lines:
            miss_rate = 0
            hit_rate = 0
            func_name = line.split(':')[0].strip()
            if '%' in line.split(':')[1]:
                miss_rate = float(line.split(':')[1].strip().split(',')[2].split("%")[0].split("'")[1])/100
                hit_rate = float(line.split(':')[1].strip().split(',')[3].strip().split(']')[0].strip().split("%")[0].split("'")[1])/100
            else:
                miss_rate = float(line.split(':')[1].strip().split(',')[2])
                hit_rate = float(line.split(':')[1].strip().split(',')[3].strip().split(']')[0].strip())
            data.append((func_name, float(miss_rate), float(hit_rate)))
    return data


def visual(data, name):
    #epoch,acc,loss,val_acc,val_loss
    x_axis_data = [func_name for func_name, _, _ in data]
    y_axis_data1 = [miss_rate for _, miss_rate, _ in data]  # miss 率
    y_axis_data2 = [hit_rate for _, _, hit_rate in data]  # hit 率
    # y_axis_data3 = [82,83,82,76,84,92,81]

            
    # 画图  
    plt.figure(figsize=(10, 6))  # 设置图形大小  
    plt.plot(x_axis_data, y_axis_data1, 'b*-', label='miss')  
    plt.plot(x_axis_data, y_axis_data2, 'rs-', label='hit')  
  
    # 设置数据标签位置及大小（可能需要调整位置以避免重叠）  
    for x, y1, y2 in zip(x_axis_data, y_axis_data1, y_axis_data2):  
        plt.text(x, y1, f'{y1:.5f}', ha='center', va='bottom', fontsize=8)  
        plt.text(x, y2, f'{y2:.5f}', ha='center', va='top', fontsize=8)  
  
    # 旋转x轴标签以避免重叠  
    plt.xticks(rotation=45, ha='right')  
    plt.legend()  
    plt.xlabel('Function Name')  
    plt.ylabel('Rate')  
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域  
  
    plt.savefig(f'f{name}.png')  


if __name__ == '__main__':
    # 主控程序
    options = my_args()
    icache_16kb_2way_64B = read_from_file(options.path)
    visual(icache_16kb_2way_64B, options.name)
