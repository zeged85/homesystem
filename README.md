#homesystem

##device instructions

###update packages
```bash
sudo apt-get update
sudo apt-get upgrade
```

##gstreamer
###install packages
```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools
```


###test camrea
```bash
gst-launch-1.0 v4l2src ! video/x-raw, width=1280, height=720, framerate=20/1 ! ximagesink
```





