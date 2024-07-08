#!/bin/bash
set -e  # 出错时立即退出
set -u  # 对未定义变量执行操作时退出

# 更新软件源
sudo apt update

# 设置工作目录和版本号
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINUTILS_DIR="$HOME/source"
BINUTILS_VERSION="2.42"
BINUTILS_TAR="binutils-${BINUTILS_VERSION}.tar.gz"
BINUTILS_URL="https://ftp.gnu.org/gnu/binutils/${BINUTILS_TAR}"

# 确保目录存在
mkdir -p "$BINUTILS_DIR"

# 切换到工作目录
cd "$BINUTILS_DIR"

# 下载 binutils 源代码
if [ ! -f "$BINUTILS_TAR" ]; then
    wget "$BINUTILS_URL"
fi

# 解压缩源代码
tar -xzvf "$BINUTILS_TAR"
cd "binutils-${BINUTILS_VERSION}"

# 配置、编译和安装
CFLAGS="-g" ./configure --prefix="$HOME/tools/binutils-${BINUTILS_VERSION}" --enable-debug
make
make install

# 清理工作目录
cd ..
# rm -rf "binutils-${BINUTILS_VERSION}"
rm "$BINUTILS_TAR"

echo "binutils ${BINUTILS_VERSION} 安装完成。"

