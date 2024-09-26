#!/bin/bash
set -e  # 出错时立即退出
set -u  # 对未定义变量执行操作时退出

# 更新软件源并安装必要依赖
sudo apt-get update
sudo apt-get install universal-ctags libgmp-dev libmpfr-dev libmpc-dev libisl-dev zlib1g-dev
sudo apt-get install --reinstall libc6-dev

# 设置工作目录和版本号
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINUTILS_DIR="$HOME/source"
GCC_VERSION="14.2.0"
GCC_TAR="gcc-${GCC_VERSION}.tar.gz"
GCC_URL="https://mirrors.nju.edu.cn/gnu/gcc/gcc-${GCC_VERSION}/${GCC_TAR}"

# 确保目录存在
mkdir -p "$BINUTILS_DIR"

# 下载 gcc 源代码并检查下载结果
if [ ! -f "$BINUTILS_DIR/$GCC_TAR" ]; then
    wget -P "$BINUTILS_DIR" "$GCC_URL"
    if [ $? -ne 0 ]; then
        echo "下载失败: $GCC_URL"
        exit 1
    fi
fi

# 切换到工作目录
cd "$BINUTILS_DIR"

# 解压缩源代码
tar -xzvf "$BINUTILS_DIR/$GCC_TAR"
cd "gcc-${GCC_VERSION}"

# 生成 ctags 标签
ctags -R

# 创建 build 目录并进入
mkdir build && cd build

# 配置、编译和安装 gcc
CFLAGS="-g -O0 -fPIC" CXXFLAGS="-g -O0 -fPIC" ../configure --prefix="$HOME/tools/gcc-${GCC_VERSION}" \
    --disable-multilib --with-ld="${HOME}/source/binutils-2.42/ld/ld-new" --enable-shared --enable-PIE
# 使用自定义LD
# CFLAGS="-O0 -g" CXXFLAGS="-O0 -g" LDFLAGS="-B /home/dushuai/source/binutils-2.42/ld/ld-new" ../configure --prefix="${HOME}/tools/gcc-14.2.0" --disable-multilib
make -j$(nproc) && make install

# 清理下载的文件和源码目录
rm -rf "$BINUTILS_DIR/$GCC_TAR"

echo "gcc ${GCC_VERSION} 安装完成。"

