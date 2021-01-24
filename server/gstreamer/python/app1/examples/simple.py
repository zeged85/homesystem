#https://gist.github.com/velovix/8cbb9bb7fe86a08fb5aa7909b2950259
from threading import Thread

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib
import time

Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()
cmd = """gst-launch-1.0.exe souphttpsrc is-live=true location="$(youtube-dl --format "best[ext=mp4][protocol=https]" --get-url https://www.youtube.com/watch?v=jQhUhlU1KL8)" ! qtdemux name=demuxer  demuxer. ! queue ! decodebin ! autovideosink  demuxer.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! autoaudiosink"""
t = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611531280&ei=sK8NYIG-BZPh1wL3opfQBg&ip=5.102.225.128&id=o-ABHwT7CcK7dWK0ygNJRUJk-NBqL2dsACBwj9OAwQfOmU&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=508750&vprv=1&mime=video%2Fmp4&ns=zrEFQGojWySkqMq0ToXK22IF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611509324&fvip=2&beids=9466587&c=WEB&txp=5532432&n=kvStZPM0GzfNsSu&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAPHyHkhW0ZGMDZPQfTg90iB0kgnzstXg4mAJBZw8jNxAAiBSU9Ne8818omKNEVDIrRpu5VjjEUeCe3YHNVJcM_eEeQ%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAOzDzS-zDzSBNdyCP19IWUg3-kbN0fTpeVYeZ09K4RQ6AiBBozHzQ3zcafBn5Xp6GrTlUPN0aYJDMF2NDlDOV_IhfA%3D%3D"""
#pipeline = Gst.parse_launch("videotestsrc ! decodebin ! videoconvert ! autovideosink")
pipeline = Gst.parse_launch(f'souphttpsrc is-live=true location="{t}" ! qtdemux name=demuxer  demuxer. ! queue ! decodebin ! autovideosink  demuxer.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! autoaudiosink')
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()