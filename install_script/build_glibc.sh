#!/bin/bash
# 更新软件源
sudo apt update

cd ~/binutils

rm -rf glibc-2.35*

# 源码下载
wget http://ftp.gnu.org/pub/gnu/glibc/glibc-2.35.tar.gz
# 解压
tar -zxf glibc-2.35.tar.gz
cd glibc-2.35
mkdir build && cd build
../configure --prefix=/home/dushuai/tools/glibc-2.35 CFLAGS="-Og -g -g3 -ggdb -gdwarf-4" CXXFLAGS="-Og -g -g3 -ggdb -gdwarf-4" --disable-werror
make -j4
make install

# 清理无用压缩包
rm -rf glibc-2.35.tar.gz

