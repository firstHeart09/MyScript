#!/bin/bash
# 本文使用GitHub上的vimplus对vim进行配置
mkdir ~/.vimplus
git clone git@github.com:chxuan/vimplus.git ~/.vimplus
cd ~/.vimplus
./install.sh //不加sudo
cd ~/.vim/plugged/YouCompleteMe
./install.sh

