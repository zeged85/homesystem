# install and setup ubuntu 

## update ubuntu
```bash
sudo apt-get update
```



## fractional scaling:
### enable 1 :
```bash
gsettings set org.gnome.mutter experimental-features "['x11-randr-fractional-scaling']"
```

### enable 2 : 
```bash
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

### disable : 
```bash
gsettings reset org.gnome.mutter experimental-features
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

## github:
```bash
sudo apt install git
```

## DVB
```bash
gst-launch-1.0 dvbbasebin modulation="QAM 64" trans-mode=8k bandwidth=8 frequency=538000000 code-rate-lp=AUTO code-rate-hp=2/3 guard=4  hierarchy=0 program-numbers=3  ! queue ! decodebin name=dmux dmux. ! queue ! audioconvert ! autoaudiosink dmux. ! queue ! autovideoconvert ! autovideosink

```




