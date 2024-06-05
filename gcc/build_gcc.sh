cd /home/dushuai/binutils
# 更新软件源
# sudo apt update
# 安装ctags
sudo apt update
sudo apt install universal-ctags 
sudo apt install libgmp-dev libmpfr-dev libmpc-dev libisl-dev zlib1g-dev
sudo apt-get install --reinstall libc6-dev
# 下载gcc-13.3.0
wget -P ~ 'https://mirrors.nju.edu.cn/gnu/gcc/gcc-13.3.0/gcc-13.3.0.tar.gz'
# 将gcc压缩包移到我的binutils目录中
mv ../gcc-13.3.0.tar.gz ./
# 对压缩包进行解压
tar xzvf gcc-13.3.0.tar.gz
# 进入gcc-13.3.0目录
cd gcc-13.3.0/
# 生成ctags标签
ctags -R
# 创建build目录
mkdir build && cd cbuild/
# 安装ubuntu32位开发库
# sudo apt-get install gcc-multilib g++-multilib
CFLAGS="-g -O0" CXXFLAGS="-g -O0" /home/dushuai/binutils/gcc-13.3.0/configure --prefix=/home/dushuai/tools/gcc-13.3.0 --disable-multilib
make -j$(nproc) && make install

# 清理源码压缩包
cd /home/dushuai/binutils
rm -rf gcc-13.3.0.tar.gz