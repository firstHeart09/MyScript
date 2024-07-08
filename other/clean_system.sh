#!/bin/bash

# 自动清理不再需要的软件包
sudo apt autoremove
# 清理APT缓存
sudo apt autoclean
# 清理已删除软件包的配置文件
sudo apt-get purge
# 清理临时文件
sudo rm -rf /tmp/*
# 清理systemd日志记录
sudo journalctl --vacuum-time=3d
# 移除旧版本的Snap应用程序
set -eu
snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        snap remove "$snapname" --revision="$revision"
    done

# 清理Ubuntu缩略图缓存
rm -rf ~/.cache/thumbnails/*
