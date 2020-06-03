# install Tensorflow 2.1 on Ubuntu 18.04 LTS with GPU support
# Nvidia Drivers, CUDA 10 and cuDNN
# TODO: opencv, gstreamer, tensorrt


# refs:
# setup GPU drivers
https://medium.com/@jonathan_hui/deep-learning-software-setup-with-gpu-bad435b85963
# install cudnn, tf
https://towardsdatascience.com/installing-nvidia-drivers-cuda-10-cudnn-for-tensorflow-2-1-on-ubuntu-18-04-lts-f1db8bff9ea
#next
http://lifestyletransfer.com/how-to-implement-object-detection-in-video-with-gstreamer-in-python-using-tensorflow/


```bash
apt install python-distutils
```

# v.2



# set gcc to v8
https://illya13.github.io/RL/tutorial/2020/04/26/installing-tensorflow-on-ubuntu-20.html

# step 1 

https://www.pyimagesearch.com/2019/12/09/how-to-install-tensorflow-2-0-on-ubuntu/

https://www.reddit.com/r/tensorflow/comments/gnjgfr/install_tensorflow_22_with_nvidia_gpu_enabled_on/


# cuda guide
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html


# cudnn guide
https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html

# tf guide
https://www.tensorflow.org/install/gpu


# step 2

https://www.pyimagesearch.com/2020/02/03/how-to-use-opencvs-dnn-module-with-nvidia-gpus-cuda-and-cudnn/



# v.3

```bash
sudo apt -y install build-essential
sudo apt -y install gcc-8 g++-8 gcc-9 g++-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8 --slave /usr/bin/g++ g++ /usr/bin/g++-8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9 --slave /usr/bin/g++ g++ /usr/bin/g++-9
sudo update-alternatives --config gcc

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential cmake unzip pkg-config
sudo apt-get install libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libopenblas-dev libatlas-base-dev liblapack-dev gfortran
sudo apt-get install libhdf5-serial-dev
sudo apt-get install python3-dev python3-tk python-imaging-tk
sudo apt-get install libgtk-3-dev

sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-driver-440
sudo apt update

sudo apt install openssh-server
sudo systemctl status ssh
sudo ufw allow ssh

sudo chmod 777 cuda
sudo chmod 777 cuDNN
sudo sh cuda_10.1.105_418.39_linux.run
more /var/log/cuda-installer.log

sudo add-apt-repository ppa:graphics-drivers
sudo apt-get update
sudo apt-get install nvidia-driver-440
sudo reboot now
nvidia-smi

nano ~/.bashrc 
```

```bash
# NVIDIA CUDA Toolkit
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64

export PATH=$PATH:/usr/local/cuda-10.1/bin

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64


# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.local/bin/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=$HOME/.local/bin/virtualenv
source $HOME/.local/bin/virtualenvwrapper.sh
```

```bash
source ~/.bashrc 
nvcc
nvcc -V

sudo dpkg -i libcudnn7_7.6.5.32-1+cuda10.1_amd64.deb
sudo dpkg -i libcudnn7-dev_7.6.5.32-1+cuda10.1_amd64.deb 
sudo dpkg -i libcudnn7-doc_7.6.5.32-1+cuda10.1_amd64.deb 
cp -r /usr/src/cudnn_samples_v7/ $HOME
cd  $HOME/cudnn_samples_v7/mnistCUDNN
make clean && make
./mnistCUDNN

tar -zxf cudnn-10.1-linux-x64-v7.6.5.32.tgz 
cd cuda
sudo cp -P lib64/* /usr/local/cuda/lib64/
sudo cp -P include/* /usr/local/cuda/include/


wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
cd ~/

pip3 install virtualenv virtualenvwrapper
nano ~/.bashrc
source ~/.bashrc 

mkvirtualenv dl4cv -p python3
workon dl4cv
pip install numpy
pip install tensorflow
python


sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt install ubuntu-restricted-extras
sudo apt install libgtk2.0-dev

sudo apt install git
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd ~/opencv
mkdir build
cd build


cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D WITH_CUDA=ON \
	-D WITH_CUDNN=ON \
	-D OPENCV_DNN_CUDA=ON \
	-D ENABLE_FAST_MATH=1 \
	-D CUDA_FAST_MATH=1 \
	-D CUDA_ARCH_BIN=6.1 \
	-D WITH_CUBLAS=1 \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D HAVE_opencv_python3=ON \
	-D PYTHON_EXECUTABLE=~/.virtualenvs/opencv_cuda/bin/python \
	-D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
	-D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
	-D WITH_GSTREAMER=ON \
	-D BUILD_EXAMPLES=ON ..
	


cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D OPENCV_ENABLE_NONFREE=ON -D WITH_CUDA=ON -D WITH_CUDNN=ON -D OPENCV_DNN_CUDA=ON -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=1 -D CUDA_ARCH_BIN=7.0 -D WITH_CUBLAS=1 -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D HAVE_opencv_python3=ON -D PYTHON_EXECUTABLE=~/.virtualenvs/opencv_cuda/bin/python -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D WITH_GSTREAMER=ON -D BUILD_EXAMPLES=ON ..


sudo make -j8
sudo make install

sudo pip install scikit-image
sudo pip install pillow
pip install imutils

cd opencv/build/
sudo make uninstall

cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D OPENCV_ENABLE_NONFREE=ON -D WITH_CUDA=ON -D WITH_CUDNN=ON -D OPENCV_DNN_CUDA=ON -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=1 -D CUDA_ARCH_BIN=6.1 -D WITH_CUBLAS=1 -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D HAVE_opencv_python3=ON -D PYTHON_EXECUTABLE=~/.virtualenvs/opencv_cuda/bin/python -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D WITH_GSTREAMER=ON -D BUILD_EXAMPLES=ON ..

sudo make -j8
sudo make install
sudo ldconfig

```bash




