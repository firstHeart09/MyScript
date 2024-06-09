#!/bin/bash
array_var=(test1 test2 test3 test4)
echo ${array_var[0]}

# 以列表形式打印出数组中的所有值
echo ${array_var[*]}
# 打印数组长度
echo ${#array_var[*]}

# 定义关联数组
# 使用声明语句将一个变量定义成关联数组
declare -A ass_array
# 添加元素
# 法一：使用行内 “索引-值”列表
ass_array=([index1]=val1 [index2]=val2)
# 法二：使用独立的“索引-值”进行赋值
ass_array[index1]=val1
ass_array[index2]=val2


