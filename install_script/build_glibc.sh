#!/bin/bash
# 更新软件源
sudo apt update

cd ~/binutils

rm -rf glibc-2.39*

# 源码下载
wget http://ftp.gnu.org/pub/gnu/glibc/glibc-2.39.tar.gz
# 解压
tar -zxf glibc-2.39.tar.gz
cd glibc-2.39
mkdir build && cd build
../configure --prefix=/home/dushuai/tools/glibc-2.39 CFLAGS="-Og -g -g3 -ggdb -gdwarf-4" CXXFLAGS="-Og -g -g3 -ggdb -gdwarf-4" --disable-werror
make -j4
make install

