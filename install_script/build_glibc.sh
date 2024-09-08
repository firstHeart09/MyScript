#!/bin/bash
set -e  # 出错时立即退出
set -u  # 对未定义变量执行操作时退出

# 更新软件源
sudo apt update
sudo apt install gawk bison
# 设置工作目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINUTILS_DIR="$HOME/source"
GLIBC_DIR="$BINUTILS_DIR/glibc-2.40"

# 确保目录存在
mkdir -p "$BINUTILS_DIR"

# 切换到工作目录
cd "$BINUTILS_DIR"

# 清理旧文件
rm -rf glibc-2.40*

# 下载 glibc 源码
wget http://ftp.gnu.org/pub/gnu/glibc/glibc-2.40.tar.gz

# 解压并编译安装
tar -zxf glibc-2.40.tar.gz
cd glibc-2.40
mkdir -p build && cd build
../configure --prefix="$HOME/tools/glibc-2.40" \
             CFLAGS="-Og -g -g3 -ggdb -gdwarf-4" \
             CXXFLAGS="-Og -g -g3 -ggdb -gdwarf-4" \
             --disable-werror \
             --enable-debug \
             --enable-debuginfod

make -j4
make install

# 清理无用文件
rm -rf "$BINUTILS_DIR/glibc-2.40.tar.gz"

echo "glibc 2.40 安装完成。"
