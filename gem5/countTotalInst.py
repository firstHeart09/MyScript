import re

def read_from_debug(path):
    """从debug.txt中读取信息到列表中"""
    data = []
    with open(path, 'r') as f_read:
        for line in f_read.readlines():
            data.append(line.strip())
    return data

def count(data):
    # 删除所有的指令改写部分
    pattern_delete_inst_ = r'\.\s?\d{1,2}'
    count = 0
    out = []  # 最后的输出数据
    for line in data:
        if 'system.cpu: T0 :' in line:
            # 说明该行是指令
            match_delete_inst_ = re.search(pattern_delete_inst_, line)
            if match_delete_inst_:
                continue
            else:
                count += 1  
    print("Total insts: ", count)

if __name__ == '__main__':
    data = []
    data = read_from_debug('./input/debug_dynamic.txt')
    count(data)