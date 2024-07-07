#!/bin/bash
set -e  # 出错时立即退出
set -u  # 对未定义变量执行操作时退出

# 更新软件源并安装必要依赖
sudo apt update
sudo apt install universal-ctags
sudo apt install libgmp-dev libmpfr-dev libmpc-dev libisl-dev zlib1g-dev
sudo apt-get install --reinstall libc6-dev

# 设置工作目录和版本号
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINUTILS_DIR="$HOME/source"
GCC_VERSION="14.1.0"
GCC_TAR="gcc-${GCC_VERSION}.tar.gz"
GCC_URL="https://mirrors.nju.edu.cn/gnu/gcc/gcc-${GCC_VERSION}/${GCC_TAR}"

# 确保目录存在
mkdir -p "$BINUTILS_DIR"

# 下载 gcc 源代码
if [ ! -f "$GCC_TAR" ]; then
    wget -P "$BINUTILS_DIR" "$GCC_URL"
fi

# 切换到工作目录
cd "$BINUTILS_DIR"

# 解压缩源代码
tar -xzvf "$GCC_TAR"
cd "gcc-${GCC_VERSION}"

# 生成 ctags 标签
ctags -R

# 创建 build 目录并进入
mkdir build && cd build

# 配置、编译和安装 gcc
CFLAGS="-g -O0" CXXFLAGS="-g -O0" ../configure --prefix="$HOME/tools/gcc-${GCC_VERSION}" --disable-multilib
make -j$(nproc) && make install

# 返回 binutils 目录并清理工作目录
cd "$BINUTILS_DIR"
rm -rf "$GCC_TAR" gcc-${GCC_VERSION}

echo "gcc ${GCC_VERSION} 安装完成。"

