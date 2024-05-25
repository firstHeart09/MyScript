#!/usr/bin/env python
# coding=utf-8

def read(filename):
    data = []
    with open(filename, 'r') as f_in:
        for line in f_in.readlines():
            if ('icache' in line and 'IF hit' in line):
                data.append(line)
            else:
                continue
    return data

if __name__ == '__main__':
    data = read('./debug_static.txt')
    print(f'if hit: {len(data)}')

