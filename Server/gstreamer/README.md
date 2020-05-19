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


## install gstreamer for linux (optional?): 
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




