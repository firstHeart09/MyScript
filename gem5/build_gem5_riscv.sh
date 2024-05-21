#!/bin/bash
set -e

cd ~/binutils/

git clone https://github.com/gem5/gem5

cd gem5/
cd .git/hooks/
cp pre-commit.sample pre-commit
cp commit-msg.sample commit-msg

cd ~/binutils/gem5

python3 `which scons` build/RISCV/gem5.opt -j7
python3 `which scons` build/X86/gem5.opt -j7
