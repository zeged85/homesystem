# install and setup ubuntu 

## update ubuntu
```bash
sudo apt-get update
```


## github:
```bash
sudo apt install git
```


## gstreamer dev
```bash
sudo apt-get install libgstreamer1.0-dev
```

### add to intllisense (path Includes in c_cpp_properties.json):
```json
"includePath": [
    "${workspaceFolder}/**",
    "/usr/include/gstreamer-1.0/**",
    "/usr/include/glib-2.0/**",
    "/usr/lib/x86_64-linux-gnu/glib-2.0/include/**"
    ]
```

## locate
## https://stackoverflow.com/questions/45401164/glib-h-no-such-file-or-directory

sudo apt install locate
updatedb
locate glib.h

## add `pkg-config --cflags --libs gstreamer-1.0` to tasks.json
## (F1: "Tasks: Configure Task Runner")
```json
"args": [
	"-g",
	"${file}",
	"-o",
	"${fileDirname}/${fileBasenameNoExtension}",
	"`",
	"pkg-config",
	"--cflags",
	"--libs",
	"gstreamer-1.0",
	"`"
    ]
```


## install gstreamer for linux: 
```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

## pytube3: 
```bash
sudo apt install python3-pip
sudo pip3 install pytube3
```



## DVB
```bash
gst-launch-1.0 dvbbasebin modulation="QAM 64" trans-mode=8k bandwidth=8 frequency=538000000 code-rate-lp=AUTO code-rate-hp=2/3 guard=4  hierarchy=0 program-numbers=3  ! queue ! decodebin name=dmux dmux. ! queue ! audioconvert ! autoaudiosink dmux. ! queue ! autovideoconvert ! autovideosink

```



# update 1
## opencv on 16.04
```bash
list=$(apt-cache --names-only search ^gstreamer1.0-* | awk '{ print $1 }' | grep -v gstreamer1.0-hybris)
sudo apt-get install $list


sudo apt install ubuntu-restricted-extras

sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev


sudo apt install python3-pip
pip3 install numpy



sudo apt install aptitude
sudo aptitude search libgtk2.0-dev
sudo aptitude install libgtk2.0-dev


sudo apt install git

git clone https://github.com/opencv/opencv.git
cd opencv/
mkdir build
cd build

sudo apt install cmake
cmake -D CMAKE_BUILD_TYPE=RELEASE -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D PYTHON_EXECUTABLE=$(which python3) -D BUILD_opencv_python2=OFF -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") -D PYTHON3_EXECUTABLE=$(which python3) -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") -D WITH_GSTREAMER=ON -D BUILD_EXAMPLES=ON ..


sudo make -j4
sudo make install
sudo ldconfig

```

