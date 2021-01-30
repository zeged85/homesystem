from gi.repository import Gtk, Gst  # ,GObject
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

class gstChannel:
    @property
    def gtksink(self):
        try:
            self._gtksink
        except Exception:
            self._gtksink = self.factory.make('gtksink')
        return self._gtksink

    def __init__(self):
        # create pipeline
        print('init pipeline')
        self._pipeline = Gst.Pipeline()

        # create gtksink by default
        self.factory = self._pipeline.get_factory()
        # ._gtksink = self.factory.make('gtksink')
        # self._testsrc()
        self.bus = self._pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        typ = message.type
        # print(typ)
        if typ == Gst.MessageType.ERROR:
            # err, debug = message.parse_error()
            # print("Error: ",err, debug)
            print('Error {}: {}, {}'.format(message.src.name, *message.parse_error()))
            # self.player.set_state(Gst.State.NULL)
        elif typ == Gst.MessageType.STATE_CHANGED:
            print(message.parse_state_changed()[1])
        else:
            print('else', typ)

    def _setCameras(self):
        def get_ksvideosrc_device_indexes():
            # https://stackoverflow.com/questions/30440134/list-device-names-available-for-video-capture-from-ksvideosrc-in-gstreamer-1-0
            device_index = 0
            video_src = Gst.ElementFactory.make('ksvideosrc')
            state_change_code = None

            while True:
                video_src.set_state(Gst.State.NULL)
                video_src.set_property('device-index', device_index)
                state_change_code = video_src.set_state(Gst.State.READY)
                if state_change_code != Gst.StateChangeReturn.SUCCESS:
                    video_src.set_state(Gst.State.NULL)
                    break
                device_index += 1
            return range(device_index)
        indexes = get_ksvideosrc_device_indexes()
        print('indexes',indexes)

        stringPipeline = """ksvideosrc device-index=0 ! videoconvert ! queue name=convert ! gtksink name=sink"""                                            
        p = Gst.parse_launch(stringPipeline) 
        self._gtksink = p.get_by_name("sink")
        self._pipeline.add(p)
        


            


    def _setUDP(self):
        # _bin = Gst.parse_bin_from_description(pipeline, True)
        # pipeline = Gst.Pipeline()
        # bus = self._pipeline.get_bus()
        # bus.add_signal_watch()
        # bus.enable_sync_message_emission()
        factory = self._pipeline.get_factory()
        # gtksink = factory.make('gtksink')

        # p = Gst.parse_launch("v4l2src ! videoconvert ! gtksink name=sink")                                             
        # p = Gst.parse_launch("videotestsrc ! videoconvert ! gtksink name=sink") 
        stringPipeline = """udpsrc uri=udp://localhost:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! queue name=convert ! gtksink name=sink"""                                            
        p = Gst.parse_launch(stringPipeline) 
        self._gtksink = p.get_by_name("sink")
        # box.pack_start(s.props.widget, ...)

        # pipeline.add(self._bin)
        self._pipeline.add(p)
        # pipeline.add(s)
        # Link the pipeline to the sink that will display the video.
        # self._bin.link(s)
        
        # self.pack_start(s.props.widget, True, True, 0)
        # s.props.widget.show()
        # Start the video
        # pipeline.set_state(Gst.State.PLAYING)

    def _setYoutube3(self):

        uri = """https://www.youtube.com/watch?v=ndl1W4ltcmg"""

        import subprocess
        proc = subprocess.Popen(
            f'youtube-dl --format "best[ext=mp4][protocol=https]" --get-url {uri}', stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        print(output)
        tst = output.decode('ascii')
        uri = tst
        player = Gst.ElementFactory.make("playbin")
        player.set_property("uri", uri)
        queue = Gst.ElementFactory.make("queue")
        bin = Gst.Bin.new("my-bin")
        bin.add(queue)
        bin.add(self._gtksink)
        pad = queue.get_static_pad("sink")
        ghostpad = Gst.GhostPad.new("sink", pad)
        bin.add_pad(ghostpad)
        # effect = Gst.ElementFactory.make("flip")
        effect = Gst.ElementFactory.make("clockoverlay", "clock")
        bin.add(effect)
        queue.link(effect)
        effect.link(self._gtksink)
        player.set_property("video-sink", bin)
        self._pipeline.add(player)
        # self._pipeline.add(queue)
        # self._pipeline.add(bin)
        # self._pipeline.add(self._gtksink)
        # player.set_state(Gst.State.PLAYING)


    def _setLocalFile(self):
        print('opening file')
        # import tkinter as tk
        # from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        # file_path = filedialog.askopenfilename()
        # filepath = ""
        location = "C:/Projects/homesystem/server/gstreamer/python/app1/examples/example.mp4"
        # print(file_path)
        # pipeline = Gst.parse_launch(f'filesrc location={file_path} ! queue ! decodebin ! autovideosink')
        t = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611587162&ei=-okOYKC5EZz_1wL98ZiYDw&ip=5.102.225.128&id=o-ANWJWezioCUiDz3tUmGq1psOOseBgr25yDgN8UVA9h-I&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pcm2cms=yes&pl=20&initcwndbps=1043750&vprv=1&mime=video%2Fmp4&ns=HZlScRQX5TsDBoD21GFonwAF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611565238&fvip=2&c=WEB&txp=5532432&n=y9E2DhdKvreEaGx&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAO26rOxkwsV7yr9PclrFUkxPJmVqYR-O-Bzka3AKYbxIAiEAk-zWjCrTAUnAAfRZCLVxk-vzcFUKN7XF3sKcqN63VM8%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAPC-gBo0CrBvVywcODWFz0XFOPYf2WmW51HZHkbuWYG1AiEApWwuxYzdPN-Y92TlzAc_wwFjLy50OBnmLkR8nY8gU7s%3D"""
        # pipeline = Gst.parse_launch(f'souphttpsrc is-live=true location="{t}" ! queue ! qtdemux ! h264parse ! d3d11h264dec ! autovideosink')
        # pipeline = Gst.Pipeline()
        # _bin = Gst.parse_bin_from_description(f'filesrc location={file_path} ! queue ! decodebin ! autovideosink', True)
        # _bin.link(self._gtksink)
        # pipeline.add(_bin)
        working = "https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm"
        player = Gst.ElementFactory.make("playbin")
        player.set_property("uri", t)
        queue = Gst.ElementFactory.make("queue")
        bin = Gst.Bin.new("my-bin")
        bin.add(queue)
        bin.add(self._gtksink)
        pad = queue.get_static_pad("sink")
        ghostpad = Gst.GhostPad.new("sink", pad)
        bin.add_pad(ghostpad)
        # effect = Gst.ElementFactory.make("flip")
        effect = Gst.ElementFactory.make("clockoverlay", "clock")
        bin.add(effect)
        queue.link(effect)
        effect.link(self._gtksink)
        player.set_property("video-sink", bin)
        # self._pipeline.add(player)
        # self._pipeline.add(queue)
        # self._pipeline.add(self._gtksink)

        # player.link(self.gtksink)
        # queue.link(self._gtksink)

        player.set_state(Gst.State.PLAYING)
        # self._pipeline.set_state(Gst.State.PLAYING)
      
    def _setLocalFile2(self):
        print('opening file')
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        # filepath = ""
        # location = "C:/Projects/homesystem/server/gstreamer/python/app1/examples/example.mp4"
        t = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611545234&ei=MuYNYKXQK4241wLjt7PACg&ip=5.102.225.128&id=o-AGvCPcdy6zY6EvN4wTDqU1psZXYD5StWNfAvAsjjUvOd&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=527500&vprv=1&mime=video%2Fmp4&ns=FQtiJUatgYVfyJhCjPRazJIF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611522765&fvip=2&c=WEB&txp=5532432&n=2048NxgmzPzdKhA&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIgVedzMJ5DZB3dp_nxQtss_6EcOdusZxbkgXAJgUIx5VYCIQD8u330fhUI6Yuhsc3_K2qGSQiJYWth9i7455KvAB8uYA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAMS2H60l73TQz8FSSMYU2SEeTNQhL-nTSK6m3a4t82y6AiEAnRqgnO27Jv5rJGlZif-tEsF4FZf7_wkncy4US0biXRU%3D"""
        print(file_path)
        # pipeline = Gst.parse_launch(f'filesrc location={file_path} ! queue ! decodebin ! autovideosink')
        # pipeline.set_state(Gst.State.PLAYING)
        source = Gst.ElementFactory.make("filesrc", "file-source")  # - fast, but singleton
        source.set_property("location", file_path)

        decode = Gst.ElementFactory.make("decodebin", "file-decode")

        def decodebin_pad_added(element, pad):
            string = pad.query_caps(None).to_string()
            print('Found stream: %s' % string)
            if string.startswith('video/x-raw'):
                print("LINKING!!!!!!!!!!!!!!!!!!!!!!!!!")
                pad.link(self._gtksink.get_static_pad('sink'))
                # decode.link(convert)
        decode.connect("pad-added", decodebin_pad_added)

        self._pipeline.add(source)
        self._pipeline.add(decode)
        self._pipeline.add(self._gtksink)

        source.link(decode)

        # decode.link(self._gtksink)

    def _setTestsrc(self):
        # desc = f'videotestsrc ! queue ! decodebin ! videoconvert ! timeoverlay !  x264enc tune=zerolatency ! rtph264pay ! udpsink host=localhost port=5000'
        desc = f'videoconvert ! queue ! x264enc tune=zerolatency ! queue ! rtph264pay ! queue ! udpsink host=localhost port=5000'
        desc = f'videoconvert ! queue ! x264enc tune=zerolatency ! queue ! rtph264pay ! queue ! multiudpsink name=mudpsink'
        # udpBin = Gst.parse_launch(desc)
        udpBin = Gst.parse_bin_from_description(desc, True)
        # return
        # DEBUG

        stringPipeline = "videotestsrc name=source"
        self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        # udpsink = Gst.ElementFactory.make("multiudpsink", "udpsink-1")
        udpsink = udpBin.get_by_name('mudpsink')
        udpsink.emit("add","localhost",5000)
        print(udpsink.props.clients)
        source = self._bin.get_by_name('source')
        print('dir source', dir(source))
        source.props.pattern = 0
        # https://stackoverflow.com/questions/47760477/python-gst-list-all-properties-of-an-element
        prop_list = udpsink.list_properties()
        # print(prop_list)
        for prop in prop_list:
            # print(prop)
            gType = str(prop)[7:].split(' ')[0]
            gName = str(prop).split("'")[1]
            status = udpsink.get_property(gName)
            print(gType,gName,status)

        # signal_list = udpsink.g_signal_list_ids()
        # for sig in signal_list:
            # print(sig)
            
            # .set_property("rotation-z",a) 

        tee = Gst.ElementFactory.make("tee", "tee-1")  # - fast, but singleton
        # autovideosink = Gst.ElementFactory.make("autovideosink", "autosink-1")  # - fast, but singleton
        autovideosink = Gst.ElementFactory.make("ximagesink", "autosink-1")  # - fast, but singleton
        
        queue1 = Gst.ElementFactory.make("queue", "queue-1")  
        queue2 = Gst.ElementFactory.make("queue", "queue-2")
        queue3 = Gst.ElementFactory.make("queue", "queue-3") 
        # queue4 = Gst.ElementFactory.make("queue", "queue-4")    
        # convert = Gst.ElementFactory.make("videoconvert", "convert-1")
        # encoder = Gst.ElementFactory.make("x264enc", "x264enc-1")
        # pay = Gst.ElementFactory.make("rtph264pay", "rtph264pay-1")
            
        self._pipeline.add(self._bin)
        self._pipeline.add(self._gtksink)
        self._pipeline.add(tee)
        self._pipeline.add(autovideosink)
        # self._pipeline.add(udpsink)
        self._pipeline.add(queue1)
        self._pipeline.add(queue2)
        self._pipeline.add(queue3)
        self._pipeline.add(udpBin)
        # self._pipeline.add(encoder)
        # self._pipeline.add(pay)
        # self._pipeline.add(convert)
        # self._pipeline.add(queue4)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(tee)
        tee.link(queue1)
        queue1.link(self._gtksink)
        tee.link(queue2)
        queue2.link(udpBin)
        # convert.link(encoder)
        # encoder.link(pay)
        # pay.link(queue4)
        # queue4.link(udpsink)
        tee.link(queue3)
        queue3.link(autovideosink)
        print('ahoy')

    def _setScreenCapture(self):
        # stringPipeline = "videotestsrc pattern=1"
        # self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        # self._src = self.factory.make('videotestsrc')
        # self.player.get_by_name("file-source").set_property("location", filepath)     
        # source = Gst.ElementFactory.make("videotestsrc", "test-source")
        # source.set_property("pattern", 1)   
        # source = Gst.ElementFactory.make("dx9screencapsrc", "test-source")
        # source = Gst.ElementFactory.make("gdiscreencapsrc", "test-source") # slow - supports multi channel


        import os
        if os.name == 'posix':
            print('linux')
            source = Gst.ElementFactory.make("ximagesrc", "test-source") # - linux
        else:  # if os.name == 'nt':
            print('windows')
            source = Gst.ElementFactory.make("dxgiscreencapsrc", "test-source") # - fast, but singleton

        if not source:
            print('source error')
            return
        # source.set_property("pattern", 1)
        # source.set_property("width", 200)
        # source.set_property("height", 200)
        # source.set_property("monitor", 0)

        convert = Gst.ElementFactory.make("videoconvert", "source-convert")
        scale = Gst.ElementFactory.make("videoscale", "source-scale")

        caps = Gst.Caps.from_string("video/x-raw, width=200,height=200")
        filter = Gst.ElementFactory.make("capsfilter", "filter")
        filter.set_property("caps", caps)

        self._pipeline.add(source)
        self._pipeline.add(filter)
        self._pipeline.add(convert)
        self._pipeline.add(scale)
        self._pipeline.add(self._gtksink)
        # Link the pipeline to the sink that will display the video.
        source.link(convert)
        convert.link(scale)
        scale.link(filter)
        filter.link(self._gtksink)

    def _setYoutube2(self):
        # import subprocess
        # proc = subprocess.Popen('youtube-dl --format "best[ext=mp4][protocol=https]" --get-url https://www.youtube.com/watch?v=ndl1W4ltcmg', stdout=subprocess.PIPE)
        # output = proc.stdout.read()
        # print(output)
        # tst = output.decode('ascii')
        # tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611440572&ei=XE0MYNb6MMSy1gKuoLroBA&ip=5.102.225.128&id=o-ABL3Py2cF11LPkGmR95rtyaNKuvw1ByfnR0Z582bnIU7&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=545000&vprv=1&mime=video%2Fmp4&ns=LuxaOK8Z-E3T4WGZaJS3AvoF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611418611&fvip=2&c=WEB&txp=5532432&n=2QXaIpEZGqGgV8H&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAKaiGKyGSn1lhhKdo14mAEQwjAwczJPf4Nufpa_uAHmbAiA6Qtd_tOEsCIMQ3VcSQUtHipeHu9uG5oyrleyn25ycwA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAID4GBxljfkGRGZXv0nk9kT7rhcvM67aDWerCXaS6fX7AiEA9IwlsN5U-Eif0o1c9OEVTB_Y3jcyx422axs4sTtpnDg%3D"""
        # tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611531280&ei=sK8NYIG-BZPh1wL3opfQBg&ip=5.102.225.128&id=o-ABHwT7CcK7dWK0ygNJRUJk-NBqL2dsACBwj9OAwQfOmU&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=508750&vprv=1&mime=video%2Fmp4&ns=zrEFQGojWySkqMq0ToXK22IF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611509324&fvip=2&beids=9466587&c=WEB&txp=5532432&n=kvStZPM0GzfNsSu&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAPHyHkhW0ZGMDZPQfTg90iB0kgnzstXg4mAJBZw8jNxAAiBSU9Ne8818omKNEVDIrRpu5VjjEUeCe3YHNVJcM_eEeQ%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAOzDzS-zDzSBNdyCP19IWUg3-kbN0fTpeVYeZ09K4RQ6AiBBozHzQ3zcafBn5Xp6GrTlUPN0aYJDMF2NDlDOV_IhfA%3D%3D"""
        # stringPipeline = f'souphttpsrc is-live=true location="{tst}" ! decodebin name = decode'
        # source = Gst.parse_launch(stringPipeline)
        # source = Gst.parse_bin_from_description(stringPipeline, True)

        # videoconvert = self.pipeline.get_by_name("convert")

        # source.link(self._gtksink)
        # self._pipeline.add(source)
        # self._pipeline.add(self._gtksink)

        t = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611545234&ei=MuYNYKXQK4241wLjt7PACg&ip=5.102.225.128&id=o-AGvCPcdy6zY6EvN4wTDqU1psZXYD5StWNfAvAsjjUvOd&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=527500&vprv=1&mime=video%2Fmp4&ns=FQtiJUatgYVfyJhCjPRazJIF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611522765&fvip=2&c=WEB&txp=5532432&n=2048NxgmzPzdKhA&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIgVedzMJ5DZB3dp_nxQtss_6EcOdusZxbkgXAJgUIx5VYCIQD8u330fhUI6Yuhsc3_K2qGSQiJYWth9i7455KvAB8uYA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAMS2H60l73TQz8FSSMYU2SEeTNQhL-nTSK6m3a4t82y6AiEAnRqgnO27Jv5rJGlZif-tEsF4FZf7_wkncy4US0biXRU%3D"""
        # pipeline = Gst.parse_launch(f'souphttpsrc is-live=true location="{t}" ! queue ! qtdemux ! h264parse ! d3d11h264dec name = dec')
        bin = Gst.parse_bin_from_description(f'souphttpsrc is-live=true location="{t}" name=source ! queue ! qtdemux ! h264parse ! d3d11h264dec name = dec',True)
        # pipeline = Gst.parse_launch("videotestsrc ! decodebin ! videoconvert ! autovideosink")
        # pipeline = Gst.parse_launch(f'souphttpsrc is-live=true location="{t}" ! qtdemux name=demuxer  demuxer. ! queue ! decodebin ! autovideosink  demuxer.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! autoaudiosink')
        # pipeline = Gst.parse_launch(f'souphttpsrc is-live=true location="{t}" ! queue ! qtdemux ! h264parse ! d3d11h264dec ! autovideosink')

        decode = bin.get_by_name("dec")

        def decodebin_pad_added(element, pad):
            string = pad.query_caps(None).to_string()
            print('Found stream: %s' % string)
            if string.startswith('video/x-raw'):
                print("LINKING!!!!!!!!!!!!!!!!!!!!!!!!!")
                # pad.link(self._gtksink.get_static_pad('sink'))
                decode.link(convert)
        decode.connect("pad-added", decodebin_pad_added)

        source = bin.get_by_name("source")

        def decodebin_pad_added(element, pad):
            string = pad.query_caps(None).to_string()
            print('Found stream: %s' % string)
            if string.startswith('video/x-raw'):
                print("LINKING!!!!!!!!!!!!!!!!!!!!!!!!!")
                # pad.link(self._gtksink.get_static_pad('sink'))
                source.link(convert)
        decode.connect("pad-added", decodebin_pad_added)

        convert = Gst.ElementFactory.make("videoconvert", "source-convert")
        scale = Gst.ElementFactory.make("videoscale", "source-scale")
        caps = Gst.Caps.from_string("video/x-raw, width=200,height=200")
        filter = Gst.ElementFactory.make("capsfilter", "filter")
        filter.set_property("caps", caps)
        self._pipeline.add(bin)
        self._pipeline.add(convert)
        self._pipeline.add(scale)
        # self._pipeline.add(caps)
        self._pipeline.add(filter)
        self._pipeline.add(self._gtksink)
        # decode.link(convert)
        convert.link(scale)
        scale.link(filter)
        filter.link(self._gtksink)

        # source = Gst.ElementFactory.make("souphttpsrc", "youtube-source")
        # source.set_property("location", t) 
        # queue = Gst.ElementFactory.make("queue", "youtube-queue")
        # demux = Gst.ElementFactory.make("qtdemux", "youtube-demux")
        # parse = Gst.ElementFactory.make("h264parse", "youtube-parse")
        # decode = Gst.ElementFactory.make("d3d11h264dec", "youtube-decode")

        # self._pipeline.add(source)
        # self._pipeline.add(queue)
        # self._pipeline.add(demux)
        # self._pipeline.add(parse)
        # self._pipeline.add(decode)
        # self._pipeline.add(self._gtksink)

        # source.link(queue)
        # queue.link(demux)
        # demux.link(parse)
        # parse.link(decode)
        # decode.link(self._gtksink)
        self._pipeline.set_state(Gst.State.PLAYING)

    def _setUDP2(self):

        """self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        print(self._bin)
        if not self._bin:
            print('source error')
            return
        self._pipeline.add(self._bin)"""

        stringPipeline = """udpsrc uri=udp://localhost:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! queue name=convert"""
        # bin = Gst.parse_bin_from_description(stringPipeline, True)
        bin = Gst.parse_launch(stringPipeline)
        self._pipeline.add(bin)
        self._pipeline.add(self._gtksink)
        bin.link(self._gtksink)
        # videoconvert = self._pipeline.get_by_name("convert")
        # self._pipeline.add(videoconvert)
        # videoconvert.link(self._gtksink)

        """source = Gst.ElementFactory.make("souphttpsrc", "youtube-source")  # - fast, but singleton
        if not source:
            print('source error')
            return
        source.set_property("is-live", True)
        source.set_property("location", tst)

        decode = Gst.ElementFactory.make("decodebin3", "youtube-decode")

        convert = Gst.ElementFactory.make("videoconvert", "youtube-convert")
        sink = Gst.ElementFactory.make("autovideosink", "youtube-sink")
        # sink = Gst.ElementFactory.make("fakesink", "youtube-sink")

        def decodebin_pad_added(element, pad):
            string = pad.query_caps(None).to_string()
            print('Found stream: %s' % string)
            if string.startswith('video/x-raw'):
                print("LINKING!!!!!!!!!!!!!!!!!!!!!!!!!")
                pad.link(sink.get_static_pad('sink'))
                # decode.link(convert)
        decode.connect("pad-added", decodebin_pad_added)
        # scale = Gst.ElementFactory.make("videoscale", "youtube-scale")

        # caps = Gst.Caps.from_string("video/x-raw, width=200,height=200")
        # filter = Gst.ElementFactory.make("capsfilter", "filter")
        # filter.set_property("caps", caps)
                  
        # src = self._pipeline.get_by_name("src")
        # print('again')
        # nl = output.decode('ascii')#[:-1]
        # print(nl)
        # src.set_property('location', nl)
        self._pipeline.add(source)
        self._pipeline.add(decode)
        self._pipeline.add(convert)
        self._pipeline.add(sink)
        # self._pipeline.add(scale)
        # self._pipeline.add(filter)
        # self._pipeline.add(self._gtksink)
        source.link(decode)
        decode.link(convert)
        convert.link(sink)
        # scale.link(filter)
        # decode.link(self._gtksink)
        # filter.link(self._gtksink)
        
        #self._pipeline.add(self._gtksink)
    
        # Link the pipeline to the sink that will display the video.
        # self._bin.link(self._gtksink)
        """
    
    def _play(self):    
        # start pipeline
        self._pipeline.set_state(Gst.State.PLAYING)

    def _stop(self):
        self._pipeline.set_state(Gst.State.NULL)

    def _setInput(self, inputType):
        # self._inputs = [["Select input"], ["test-src"], ["local file"], ["DVB"], ["Screen Capture"], ["USB-Camera"], ["UDP"], ["TCP"], ["RTSP"], ["Audio"]]
        print(f'input set to {inputType}')
        if inputType == "test-src":
            print('setting videotestsec')
            self._setTestsrc()
        elif inputType == 'DVB':
            print('DVB')
        elif inputType == 'Screen Capture':
            print('screen capture')
            self._setScreenCapture()
        elif inputType == 'youtube':
            print('youtube')
            self._setYoutube3()
        elif inputType == 'local file':
            print('local file 2')
            print('calling')
            self._setLocalFile()
            print('called')
        elif inputType == 'UDP':
            print('UDP')
            self._setUDP()
        elif inputType=='USB-Camera':
            print('camera')
            self._setCameras()

