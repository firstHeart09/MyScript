#!/bin/bash

# 终止脚本执行当遇到错误
set -e

# 安装必要工具
echo "更新软件包列表并安装必要的工具..."
sudo apt-get update
sudo apt-get install -y build-essential libgmp-dev libmpfr-dev libmpc-dev flex bison libisl-dev

# 定义版本和路径
BINUTILS_VERSION="2.34"
GCC_VERSION="9.4.0"
INSTALL_DIR="$HOME/tools"
SOURCE_DIR="$HOME/source"

# 清理旧文件
echo "删除旧的安装文件..."
rm -rf "${INSTALL_DIR}/gcc-${GCC_VERSION}" "${INSTALL_DIR}/binutils-${BINUTILS_VERSION}"
rm -rf "${SOURCE_DIR}/gcc-${GCC_VERSION}*" "${SOURCE_DIR}/binutils-${BINUTILS_VERSION}*"

# 创建源码安装目录（如果不存在）
mkdir -p "$SOURCE_DIR"
cd "$SOURCE_DIR"

# 安装 binutils
if [ ! -d "binutils-$BINUTILS_VERSION" ]; then
    echo "下载 binutils-$BINUTILS_VERSION..."
    wget --retry-connrefused --waitretry=1 --timeout=20 "https://ftp.gnu.org/gnu/binutils/binutils-$BINUTILS_VERSION.tar.gz"
    echo "解压 binutils..."
    tar -zxvf "binutils-$BINUTILS_VERSION.tar.gz"
fi

cd "binutils-$BINUTILS_VERSION/"
mkdir -p build && cd build

echo "配置 binutils..."
CFLAGS="-g" ../configure --prefix="$INSTALL_DIR/binutils-$BINUTILS_VERSION" --enable-debug --enable-gold

# 编译并安装
echo "编译和安装 binutils..."
make -j"$(nproc)" && make install

# 验证 binutils 安装
if command -v ld &> /dev/null; then
    echo "binutils 安装成功，ld 可用。"
else
    echo "binutils 安装失败，请检查错误信息。"
    exit 1
fi

# 删除下载的文件
cd "$SOURCE_DIR"
rm -f "binutils-$BINUTILS_VERSION.tar.gz"

# 进入源码安装目录
cd "$SOURCE_DIR"

# 安装 gcc
if [ ! -d "gcc-$GCC_VERSION" ]; then
    echo "下载 gcc-$GCC_VERSION..."
    wget --retry-connrefused --waitretry=1 --timeout=20 "https://mirrors.nju.edu.cn/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.gz"
    echo "解压 gcc..."
    tar -zxvf "gcc-$GCC_VERSION.tar.gz"
fi

cd "gcc-$GCC_VERSION/"
mkdir -p build && cd build

echo "配置 gcc..."
CFLAGS="-g -O0" CXXFLAGS="-g -O0" ../configure \
	--prefix="$INSTALL_DIR/gcc-$GCC_VERSION" \
	--disable-multilib \
	--with-ld="${SOURCE_DIR}/binutils-${BINUTILS_VERSION}/build/ld/ld-new" \
	--with-as="${SOURCE_DIR}/binutils-${BINUTILS_VERSION}/build/gas/as-new"

# 编译并安装
echo "编译和安装 gcc..."
make -j"$(nproc)" && make install

# 验证 gcc 安装
if command -v gcc &> /dev/null; then
    echo "gcc 安装成功，gcc 可用。"
else
    echo "gcc 安装失败，请检查错误信息。"
    exit 1
fi

# 删除下载的文件
cd "$SOURCE_DIR"
rm -f "gcc-$GCC_VERSION.tar.gz"

echo "Binutils和GCC安装完成！"
