#!/bin/bash

# 设置LLVM源码路径
LLVM_SOURCE=$HOME/source

# 确保源码目录存在
mkdir -p $LLVM_SOURCE || { echo "创建源码目录失败"; exit 1; }

# 进入源码安装目录
cd $LLVM_SOURCE || { echo "进入源码目录失败"; exit 1; }

# 克隆LLVM项目
git clone https://github.com/llvm/llvm-project.git || { echo "克隆LLVM项目失败"; exit 1; }

# 进入项目目录
cd llvm-project || { echo "进入LLVM项目目录失败"; exit 1; }

# 创建build文件夹并进入
mkdir build || { echo "创建build目录失败"; exit 1; }
cd build || { echo "进入build目录失败"; exit 1; }

# 运行cmake配置
cmake -G Ninja ../llvm-project/llvm \
      -DLLVM_TARGETS_TO_BUILD="X86;AArch64" \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_ENABLE_ASSERTIONS=ON \
      -DLLVM_ENABLE_PROJECTS="bolt" || { echo "CMake配置失败"; exit 1; }

# 编译bolt项目
ninja bolt || { echo "编译bolt项目失败"; exit 1; }

echo "LLVM项目克隆并编译成功"

