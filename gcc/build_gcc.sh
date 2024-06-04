cd /home/dushuai/binutils
# 更新软件源
# sudo apt update
# 安装ctags
sudo apt install universal-ctags
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
mkdir myfile && cd myfile
mkdir build install
cd build/
# 安装ubuntu32位开发库
# sudo apt-get install gcc-multilib g++-multilib
CFLAGS="-g -O0" CXXFLAGS="-g -O0" ../../configure --prefix=/home/dushuai/binutils/gcc-13.1.0/myfile/install/ --enable-multilib
make -j8 && make install