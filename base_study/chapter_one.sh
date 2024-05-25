#!/bin/bash

echo "hello world !"
echo hello world !
echo 'hello world !'

fruit=apple
count=5
echo "we have ${count} ${fruit}(s)"

# 添加一条新路径
# 法一
# export PATH="${PATH}:/home/user/bin"
# 法二
# PATH="${PATH}:/home/user/bin"
export PATH

if [ ${UID} -ne 0 ]; then
    echo no root user
else
    echo root user
fi

# 可以像为变量分配字符串值那样为其分配数值
no1=4
no2=5
# let命令可以执行执行基本的算术操作。当使用let命令时，变量名前不需要在添加$
let result=no1+no2
echo ${result}
# []操作符的使用方法与let命令一样
result=$[no1*no2]
echo ${result}
# (())操作符，出现在该操作符中的变量名之前需要加上$
result=$((no1+50))
echo ${result}
# expr同样可以用于基本算术操作
result=`expr 3+5`
echo $result

