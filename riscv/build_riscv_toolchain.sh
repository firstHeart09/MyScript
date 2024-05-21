#!/bin/bash

set -e

PREFIX="$HOME/tools/riscv"

cd ~/binutils/

# git clone --recursive https://github.com/riscv/riscv-gnu-toolchain

cd riscv-gnu-toolchain

./configure --prefix="${PREFIX}" --enable-multilib
make newlib -j $(nproc)
make linux -j $(nproc)

export PATH="$PATH:$PREFIX/bin"
export RISCV="$PREFIX"

echo If you want to use it in future works, add
echo
echo export PATH=\"\$PATH:$PREFIX/bin\"
echo export RISCV=\"$PREFIX\"
echo
echo to your \'.bashrc\' file.

