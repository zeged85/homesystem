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
        self._view.connect('destroy', self.on_destroy)
        self._channels = []
        

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

        self._model._setTestsrc(channelNum)




        



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









class myView(Gtk.Window):
    # https://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html
    # emit w/ args
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'button-stopChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }
    def __init__(self, **kw):
        super(myView, self).__init__(default_width=200, default_height=200, **kw)
        #self.window = Gtk.ApplicationWindow()
        self._channels = -1
        self.hbox = Gtk.HBox()
        self.add(self.hbox)



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
        vbox.add(hbox_transport)
        # start
        button_start = Gtk.Button(label = "Start")
        button_start.connect("clicked", self._button_startChannel_pressed,channelNumber)
        hbox_transport.add(button_start)
        # stop
        button_stop = Gtk.Button(label = "Stop")
        button_stop.connect("clicked", self._button_stopChannel_pressed,channelNumber)
        hbox_transport.add(button_stop)

        

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

    def _setTestsrc(self):
        stringPipeline = "videotestsrc"
        self._bin = Gst.parse_bin_from_description(stringPipeline, True)
        self._pipeline.add(self._bin)
        self._pipeline.add(self.gtksink)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(self.gtksink)

    
    def _play(self):    
        # start pipeline
        self._pipeline.set_state(Gst.State.PLAYING)

    def _stop(self):
        self._pipeline.set_state(Gst.State.NULL)




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