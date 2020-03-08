# setup android-studio w/ gstreamer


from link 1
https://stackoverflow.com/questions/54911219/gstreamer-android-tutorial-build-failed

Android Studio 3.5. For Windows 10, w/ gstreamer tutorials

tested w/:
NDK r18
binaries - gstreamer-1.0-android-universal-1.16.2
gst-docs-1.16 (last commit https://gitlab.freedesktop.org/gstreamer/gst-docs/-/commit/af9e42d13048abedd22c034e13abc848179df72b is broken. use one before: https://gitlab.freedesktop.org/gstreamer/gst-docs/-/commit/254ce57b071da11132678b7a5b31bbf1a5b21c88


    compileSdkVersion 23
    buildToolsVersion '27.0.3'
	        minSdkVersion 15
        targetSdkVersion 15




obsolete link 2
https://stackoverflow.com/questions/45044210/gstreamer-examples-in-android-studio




Add
```makefile
GSTREAMER_PLUGINS         := $(GSTREAMER_PLUGINS_CORE) $(GSTREAMER_PLUGINS_SYS) $(GSTREAMER_PLUGINS_EFFECTS) $(GSTREAMER_PLUGINS_CODECS_RESTRICTED) $(GSTREAMER_PLUGINS_NET) $(GSTREAMER_PLUGINS_PLAYBACK) $(GSTREAMER_PLUGINS_CODECS)
```
to Android.mk file to enable relevant plugins


add permissions to enable networking
```xml
    <uses-sdk android:minSdkVersion="9" android:targetSdkVersion="14"/>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-feature android:glEsVersion="0x00020000"/>
```



change tutorial 3

```c
data->pipeline =
      gst_parse_launch ("udpsrc port=5000 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, sprop-parameter-sets=\\\"J2QAKKwrQCgC3YCA8SJq\\\\,KO4BNyw\\\\=\\\", payload=96\" ! queue ! rtph264depay  ! queue ! decodebin ! videoconvert ! autovideosink", &error);
```
