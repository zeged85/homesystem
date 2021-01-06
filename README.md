# homesystem

## device instructions


### update packages
```bash
sudo apt-get update
sudo apt-get upgrade
```

install git
curl or wget this rep
git clone
than install w/ .sh



## gstreamer
### install packages
```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools
```


### test camera
```bash
gst-launch-1.0 v4l2src ! video/x-raw, width=1280, height=720, framerate=20/1 ! ximagesink
```


flip camera


### send h264 over udp
```bash
gst-launch-1.0 -v v4l2src  ! video/x-raw, width=1280, height=720, framerate=20/1 ! videoscale ! videoconvert ! omxh264enc control-rate=variable target-bitrate=1000000 ! rtph264pay ! udpsink host=10.100.102.20 port=5000
```

### reciever code
```bash
gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
```

## Windows
```
gst-launch-1.0 mfvideosrc device-path="\\\\\?\\usb\#vid_0403\&pid_602b\&mi_00\#6\&38a650e4\&0\&0000\#\{e5323777-f976-4f5b-9b55-b94699c46e44\}\\global" ! decodebin ! videoconvert !  x264enc tune=zerolatency pass=5 quantizer=25 speed-preset=6 bitrate=100000 ! rtph264pay ! queue ! udpsink host=10.0.0.12 port=5000
```
ksvideosrc 
avfvideosrc 

### gst-device-monitor-1.0 - finding devices paths
```
gst-device-monitor-1.0 
```



### iOS

### OSX recieve - udpsec + uri
```
./gst-launch-1.0 -v udpsrc uri=udp://10.0.0.12:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
```
### send
```
./gst-launch-1.0 videotestsrc ! decodebin ! videoconvert ! x264enc tune=zerolatency ! rtph264pay ! udpsink host=10.0.0.12 port=5000
```

### relay
```
./gst-launch-1.0 -v udpsrc uri=udp://10.0.0.12:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! queue ! udpsink host=10.0.0.85 port=5000
```