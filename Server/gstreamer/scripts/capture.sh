#!/bin/bash
gst-launch-1.0 gdiscreencapsrc x=100 y=100 width=320 height=240 cursor=TRUE ! videoconvert ! dshowvideosink