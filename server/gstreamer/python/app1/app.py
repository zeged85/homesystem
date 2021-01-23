#https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, GObject, Gst
Gst.init(None)
Gst.init_check(None)


class GstWidget(Gtk.Box):
    def __init__(self, gtksink):
        super().__init__()
        # Only setup the widget after the window is shown.
        self.connect('realize', self._on_realize)

        self.gtksink = gtksink

        # Parse a gstreamer pipeline and create it.
        #self._bin = Gst.parse_bin_from_description(stringPipeline, True)

    def _on_realize(self, widget):
        #pipeline = Gst.Pipeline()
        #factory = pipeline.get_factory()
        #gtksink = factory.make('gtksink')
        #pipeline.add(self._bin)
        #pipeline.add(gtksink)
        # Link the pipeline to the sink that will display the video.
        #self._bin.link(gtksink)
        self.pack_start(self.gtksink.props.widget, True, True, 0)
        self.gtksink.props.widget.show()
        # Start the video
        #pipeline.set_state(Gst.State.PLAYING)




class myController(object):
    def __init__(self,view,model):
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
        #self._channels.append(channel)
        _gtksink = self._model._getGtksink(channelNum)
        #_gtksink = channel.gtksink

        # standalone
        #pipeline = Gst.Pipeline()

        # create and send gtksink to view
        #factory = pipeline.get_factory()
        #gtksink = factory.make('gtksink')
        self._view._addVideoView(_gtksink)

        #self._model._setTestsrc(channelNum)




        



    def _startVideo(self,button, channelNum):
        print("starting video",channelNum)
        #channel = self._channels[arg]
        #channel._stop()
        self._model._play(channelNum)

    def _stopVideo(self,button, channelNum):
        print("stopping video",channelNum)
        #channel = self._channels[arg]
        self._model._stop(channelNum)
        #channel._play()

    def _inputChanged(self,combo,channelNum, inputType):
        print("input changed")
        #print(combo)
        print("channel",channelNum)
        print("input",inputType)

        self._model._setInput(channelNum,inputType)







class myView(Gtk.Window):
    # https://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html
    # emit w/ args
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'button-stopChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'combobox-input-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,str,))
    }
    def __init__(self, **kw):
        super(myView, self).__init__(default_width=200, default_height=200, **kw)
        #self.window = Gtk.ApplicationWindow()
        self._channels = -1
        self.hbox = Gtk.HBox()
        self.add(self.hbox)
        
        # TODO: popUP - for local file browser
        self._inputs = [["Select input"], ["test-src"], ["local file"], ["DVB"], ["Screen Capture"], ["USB-Camera"], ["youtube"], ["torrent"], ["UDP"], ["TCP"], ["RTSP"], ["Audio"]]



        # self.window.connect('destroy', on_destroy)

        self._setup()
        self._update()

    def _setup(self):
        button_addChannel = Gtk.Button(label = "Add channel")
        button_addChannel.connect("clicked", self._button_addChannel_pressed)
        self.hbox.add(button_addChannel)

    def _update(self):
        self.show_all()

    def _button_addChannel_pressed(self,obj):
        print("VIEW: button-addChannel-pressed")
        self.emit('button-addChannel-clicked')

    def _button_startChannel_pressed(self,obj,arg):
        print(f"VIEW: button-startChannel-pressed",arg)
        self.emit('button-startChannel-clicked',int(arg))

    def _button_stopChannel_pressed(self,obj,arg):
        print(f"VIEW: button-stopChannel-pressed",arg)
        self.emit('button-stopChannel-clicked',int(arg))



    def on_changed(self, combo, channelNum):
        # if the row selected is not the first one, write its value on the
        # terminal
        if combo.get_active() != 0:
            inputType = str(self._inputs[combo.get_active()][0])
            print("You chose " + str(self._inputs[combo.get_active()][0]) + ".")
            self.emit('combobox-input-changed',int(channelNum),str(inputType))

        return True


    def _addVideoView(self,gtksink):
        #print(obj)
        #print(type(obj))
        print("add video")
        #widget = GstWidget('videotestsrc pattern=1')
        self._channels+=1
        channelNumber = self._channels

        # Video View
        widget = GstWidget(gtksink)
        widget.set_size_request(200, 200)
        vbox = Gtk.VBox()
        vbox.add(widget)

        # Start / Stop Buttons - transport layer
        hbox_transport = Gtk.HBox()
        # start
        button_start = Gtk.Button(label = "Start")
        button_start.connect("clicked", self._button_startChannel_pressed,channelNumber)
        hbox_transport.add(button_start)
        # stop
        button_stop = Gtk.Button(label = "Stop")
        button_stop.connect("clicked", self._button_stopChannel_pressed,channelNumber)
        hbox_transport.add(button_stop)

        vbox.add(hbox_transport)
        # ComboBox
        # TODO: move to own class

        listmodel = Gtk.ListStore(str)
        # append the data in the model
        for i in range(len(self._inputs)):
            listmodel.append(self._inputs[i])

        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(0)

        # connect the signal emitted when a row is selected to the callback
        # function
        combobox.connect("changed", self.on_changed, channelNumber)

        # add the combobox to the window
        vbox.add(combobox)


        

        self.hbox.add(vbox)

        #self.window.show_all()
        self._update()


class gstChannel:
    @property
    def gtksink(self):
        try:
            self._gtksink
        except:
            self._gtksink = self.factory.make('gtksink')
        return self._gtksink

    def __init__(self):
        # create pipeline
        self._pipeline = Gst.Pipeline()

        # create gtksink by default
        self.factory = self._pipeline.get_factory()
        #self._gtksink = self.factory.make('gtksink')
        #self._testsrc()
        self.bus = self._pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

    def on_message(self, bus, message):
            typ = message.type
            print(typ)
            err, debug = message.parse_error()
            print("Error: ",err, debug)
            print('Error {}: {}, {}'.format(message.src.name, *message.parse_error()))
            #self.player.set_state(Gst.State.NULL)

    def _setTestsrc(self):
        stringPipeline = "videotestsrc"
        self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        self._pipeline.add(self._bin)
        self._pipeline.add(self._gtksink)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(self._gtksink)

    def _setScreenCapture(self):
        #stringPipeline = "videotestsrc pattern=1"
        #self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        #self._src = self.factory.make('videotestsrc')
        #self.player.get_by_name("file-source").set_property("location", filepath)
        
        #source = Gst.ElementFactory.make("videotestsrc", "test-source")
        #source.set_property("pattern", 1)
        
        #source = Gst.ElementFactory.make("dx9screencapsrc", "test-source")
        #source = Gst.ElementFactory.make("gdiscreencapsrc", "test-source") # slow - supports multi channel
        source = Gst.ElementFactory.make("dxgiscreencapsrc", "test-source") # - fast, but singleton
        if not source:
            print('source error')
            return
        #source.set_property("pattern", 1)
        #source.set_property("width", 200)
        #source.set_property("height", 200)
        #source.set_property("monitor", 0)


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

    def _setYoutube(self):
        import subprocess
        #proc = subprocess.Popen('youtube-dl --format "best[ext=mp4][protocol=https]" --get-url https://www.youtube.com/watch?v=ndl1W4ltcmg', stdout=subprocess.PIPE)
        #output = proc.stdout.read()
        #print(output)
        #tst = output.decode('ascii')
        tst = """https://r2---sn-m4vox-ua8s.googlevideo.com/videoplayback?expire=1611440572&ei=XE0MYNb6MMSy1gKuoLroBA&ip=5.102.225.128&id=o-ABL3Py2cF11LPkGmR95rtyaNKuvw1ByfnR0Z582bnIU7&itag=22&source=youtube&requiressl=yes&mh=eV&mm=31%2C29&mn=sn-m4vox-ua8s%2Csn-4g5edne7&ms=au%2Crdu&mv=m&mvi=2&pl=20&initcwndbps=545000&vprv=1&mime=video%2Fmp4&ns=LuxaOK8Z-E3T4WGZaJS3AvoF&ratebypass=yes&dur=140.387&lmt=1572989225009924&mt=1611418611&fvip=2&c=WEB&txp=5532432&n=2QXaIpEZGqGgV8H&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAKaiGKyGSn1lhhKdo14mAEQwjAwczJPf4Nufpa_uAHmbAiA6Qtd_tOEsCIMQ3VcSQUtHipeHu9uG5oyrleyn25ycwA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAID4GBxljfkGRGZXv0nk9kT7rhcvM67aDWerCXaS6fX7AiEA9IwlsN5U-Eif0o1c9OEVTB_Y3jcyx422axs4sTtpnDg%3D"""
        stringPipeline = f'souphttpsrc is-live=true location="{tst}" ! decodebin ! videoconvert ! videoscale ! autovideosink'
        
        #stringPipeline = f'souphttpsrc is-live=true name=src ! decodebin ! videoconvert'
        """self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        print(self._bin)
        if not self._bin:
            print('source error')
            return
        self._pipeline.add(self._bin)"""

        source = Gst.ElementFactory.make("souphttpsrc", "youtube-source") # - fast, but singleton
        if not source:
            print('source error')
            return
        source.set_property("is-live", True)
        source.set_property("location", tst)

        decode = Gst.ElementFactory.make("decodebin", "youtube-decode")
        convert = Gst.ElementFactory.make("videoconvert", "youtube-convert")
        #scale = Gst.ElementFactory.make("videoscale", "youtube-scale")

        #caps = Gst.Caps.from_string("video/x-raw, width=200,height=200")
        #filter = Gst.ElementFactory.make("capsfilter", "filter")
        #filter.set_property("caps", caps)
                  
        #src = self._pipeline.get_by_name("src")
        #print('again')
        #nl = output.decode('ascii')#[:-1]
        #print(nl)
        #src.set_property('location', nl)
        self._pipeline.add(source)
        self._pipeline.add(decode)
        self._pipeline.add(convert)
        #self._pipeline.add(scale)
        #self._pipeline.add(filter)
        self._pipeline.add(self._gtksink)
        decode.link(convert)
        convert.link(self._gtksink)
        #scale.link(filter)
        #scale.link(self._gtksink)
        #filter.link(self._gtksink)
    
        # Link the pipeline to the sink that will display the video.
        #self._bin.link(self._gtksink)
    
    def _play(self):    
        # start pipeline
        self._pipeline.set_state(Gst.State.PLAYING)

    def _stop(self):
        self._pipeline.set_state(Gst.State.NULL)

    def _setInput(self,inputType):
        #self._inputs = [["Select input"], ["test-src"], ["local file"], ["DVB"], ["Screen Capture"], ["USB-Camera"], ["UDP"], ["TCP"], ["RTSP"], ["Audio"]]
        if inputType == "test-src":
            print('setting videotestsec')
            self._setTestsrc()
        elif inputType == 'local file':
            print('local file')
        elif inputType == 'DVB':
            print('DVB')
        elif inputType == 'Screen Capture':
            print('screen capture')
            self._setScreenCapture()
        elif inputType == 'youtube':
            print('youtube')
            self._setYoutube()






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

    def _getGtksink(self,channelNum):
        return self._channels[channelNum].gtksink

    def _setTestsrc(self,channelNum):
        self._channels[channelNum]._setTestsrc()

    def _play(self,channelNum):
        self._channels[channelNum]._play()
        
    def _stop(self,channelNum):
        self._channels[channelNum]._stop()

    def _setInput(self,channelNum,inputType):
        self._channels[channelNum]._setInput(inputType)





if __name__ == "__main__":
        

    # window = Gtk.ApplicationWindow()

    view = myView()
    model = myModel()


    # vbox = Gtk.VBox()

    # window
    # window.add(vbox)

    # model
    controller = myController(view,model)

    # Create a gstreamer pipeline with no sink. 
    # A sink will be created inside the GstWidget.
    #widget = GstWidget('videotestsrc')
    #widget.set_size_request(200, 200)

    #vbox.add(widget)
    #button = Gtk.Button("Start")
    #button.connect("clicked", controller.addVideo)
    #vbox.add(button)

    #window.show_all()




    Gtk.main()