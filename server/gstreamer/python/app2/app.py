# https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
from gi.repository import Gtk, Gst  # ,GObject
import gi
from view import myView

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

Gst.init(None)
Gst.init_check(None)


class myController(object):
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._view.connect('button-addChannel-clicked', self._addVideo)
        self._view.connect('button-startChannel-clicked', self._startVideo)
        self._view.connect('button-stopChannel-clicked', self._stopVideo)
        self._view.connect('combobox-input-changed', self._inputChanged)
        self._view.connect('destroy', self.on_destroy)

    def on_destroy(self, win):
        Gtk.main_quit()

    def _addVideo(self, button):
        # model
        channelNum = self._model._createChannel()
        # self._channels.append(channel)
        _gtksink = self._model._getGtksink(channelNum)
        self._view._addVideoView(_gtksink)

    def _startVideo(self, button, channelNum):
        print("starting video", channelNum)
        # channel = self._channels[arg]
        # channel._stop()
        self._model._play(channelNum)

    def _stopVideo(self, button, channelNum):
        print("stopping video", channelNum)
        # channel = self._channels[arg]
        self._model._stop(channelNum)
        # channel._play()

    def _inputChanged(self, combo, channelNum, inputType):
        print("input changed")
        # print(combo)
        print("channel", channelNum)
        print("input", inputType)

        self._model._setInput(channelNum, inputType)


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

    def _setYoutube3(self):
        import subprocess
        proc = subprocess.Popen(
            'youtube-dl --format "best[ext=mp4][protocol=https]" --get-url \
                https://www.youtube.com/watch?v=ndl1W4ltcmg \
                    ', stdout=subprocess.PIPE)
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
        player.set_state(Gst.State.PLAYING)


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
        stringPipeline = "videotestsrc"
        self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        self._pipeline.add(self._bin)
        self._pipeline.add(self._gtksink)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(self._gtksink)

    def _setScreenCapture(self):
        # stringPipeline = "videotestsrc pattern=1"
        # self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        # self._src = self.factory.make('videotestsrc')
        # self.player.get_by_name("file-source").set_property("location", filepath)     
        # source = Gst.ElementFactory.make("videotestsrc", "test-source")
        # source.set_property("pattern", 1)   
        # source = Gst.ElementFactory.make("dx9screencapsrc", "test-source")
        # source = Gst.ElementFactory.make("gdiscreencapsrc", "test-source") # slow - supports multi channel
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

    def _setYoutube(self):
        # import subprocess
        # proc = subprocess.Popen('youtube-dl --format "best[ext=mp4][protocol=https]" --get-url https://www.youtube.com/watch?v=ndl1W4ltcmg', stdout=subprocess.PIPE)
        # output = proc.stdout.read()
        # print(output)
        # tst = output.decode('ascii')
        # tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611440572&ei=XE0MYNb6MMSy1gKuoLroBA&ip=5.102.225.128&id=o-ABL3Py2cF11LPkGmR95rtyaNKuvw1ByfnR0Z582bnIU7&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=545000&vprv=1&mime=video%2Fmp4&ns=LuxaOK8Z-E3T4WGZaJS3AvoF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611418611&fvip=2&c=WEB&txp=5532432&n=2QXaIpEZGqGgV8H&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAKaiGKyGSn1lhhKdo14mAEQwjAwczJPf4Nufpa_uAHmbAiA6Qtd_tOEsCIMQ3VcSQUtHipeHu9uG5oyrleyn25ycwA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAID4GBxljfkGRGZXv0nk9kT7rhcvM67aDWerCXaS6fX7AiEA9IwlsN5U-Eif0o1c9OEVTB_Y3jcyx422axs4sTtpnDg%3D"""
        tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611531280&ei=sK8NYIG-BZPh1wL3opfQBg&ip=5.102.225.128&id=o-ABHwT7CcK7dWK0ygNJRUJk-NBqL2dsACBwj9OAwQfOmU&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=508750&vprv=1&mime=video%2Fmp4&ns=zrEFQGojWySkqMq0ToXK22IF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611509324&fvip=2&beids=9466587&c=WEB&txp=5532432&n=kvStZPM0GzfNsSu&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAPHyHkhW0ZGMDZPQfTg90iB0kgnzstXg4mAJBZw8jNxAAiBSU9Ne8818omKNEVDIrRpu5VjjEUeCe3YHNVJcM_eEeQ%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAOzDzS-zDzSBNdyCP19IWUg3-kbN0fTpeVYeZ09K4RQ6AiBBozHzQ3zcafBn5Xp6GrTlUPN0aYJDMF2NDlDOV_IhfA%3D%3D"""
        # stringPipeline = f'souphttpsrc is-live=true location="{tst}" ! decodebin ! videoconvert'
        # stringPipeline = f'souphttpsrc is-live=true location="{tst}" ! decodebin ! videoconvert ! videoscale'     
        # stringPipeline = f'souphttpsrc is-live=true name=src ! decodebin ! videoconvert'
        """self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        print(self._bin)
        if not self._bin:
            print('source error')
            return
        self._pipeline.add(self._bin)"""

        source = Gst.ElementFactory.make("souphttpsrc", "youtube-source")  # - fast, but singleton
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


class myModel:
    @property
    def greetee(self):
        return 'World'

    def __init__(self):
        self._channels = []

    def _createChannel(self):
        print("model add (create) channel")

        channel = gstChannel()
        self._channels.append(channel)

        return (len(self._channels)-1)

    def _getGtksink(self, channelNum):
        return self._channels[channelNum].gtksink

    def _setTestsrc(self, channelNum):
        self._channels[channelNum]._setTestsrc()

    def _play(self, channelNum):
        self._channels[channelNum]._play()

    def _stop(self, channelNum):
        self._channels[channelNum]._stop()

    def _setInput(self, channelNum, inputType):
        self._channels[channelNum]._setInput(inputType)


if __name__ == "__main__":
    # window = Gtk.ApplicationWindow()

    view = myView()
    model = myModel()

    # vbox = Gtk.VBox()

    # window
    # window.add(vbox)

    # model
    controller = myController(view, model)

    # Create a gstreamer pipeline with no sink. 
    # A sink will be created inside the GstWidget.
    # widget = GstWidget('videotestsrc')
    # widget.set_size_request(200, 200)

    # vbox.add(widget)
    # button = Gtk.Button("Start")
    # button.connect("clicked", controller.addVideo)
    # vbox.add(button)

    # window.show_all()

Gtk.main()
