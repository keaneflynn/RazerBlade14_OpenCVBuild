sudo apt update
sudo apt upgrade

sudo apt install -y gcc-10 g++-10
sudo apt install -y build-essential cmake pkg-config yasm git checkinstall
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev 
sudo apt install -y libxvidcore-dev x264 libx264-dev libfaac-dev libmp3lame-dev libtheora-dev 
sudo apt install -y libfaac-dev libmp3lame-dev libvorbis-dev
sudo apt-get install -y libavresample-dev libdc1394-22 libdc1394-22-dev libxine2-dev libv4l-dev v4l-utils

mkdir opencv_build && cd opencv_build
wget -O opencv.zip https://github.com/opencv/opencv/archive/refs/tags/4.5.3.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/refs/tags/4.5.3.zip
unzip opencv.zip
unzip opencv_contrib.zip

echo "Moving onto the build portion of things"
cd opencv-4.5.3
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_C_COMPILER=/usr/bin/gcc-10 \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D OPENCV_GENERATE_PKGCONFIG=ON \
	-D BUILD_opencv_python3=ON \
	-D CUDA_ARCH_BIN=8.6 \
	-D WITH_CUDA=ON \
	-D WITH_CUDNN=ON \
	-D OPENCV_DNN_CUDA=ON \
	-D ENABLE_FAST_MATH=1 \
	-D CUDA_FAST_MATH=1 \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D WTIH_CUBLAS=1 \
	-D WITH_V4L=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib-4.5.3/modules ..
	
echo "Configuring build & making OpenCV"

make -j$(nproc)
sudo make install

