#!/usr/bin/env python
# coding=utf-8
import re
def read_from_debug(path):
    data = []  # 保存读取进来的数据的列表
    with open(path, 'r') as f_in:
        for line in f_in.readlines():
            if 'icache' in line and 'access for ReadReq' in line and 'IF miss' in line:
                data.append(line)
            else:
                continue
    return data

if __name__ == '__main__':
    data = read_from_debug('./debug_static.txt')
    print(f"num of if miss: {len(data)}")
