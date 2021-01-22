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
        self._view.connect('destroy', self.on_destroy)

    def on_destroy(self, win):
        Gtk.main_quit()

    def _addVideo(self, button):
        pipeline = Gst.Pipeline()

        # create and send gtksink to view
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        self._view._addVideoView(gtksink)


        # model
        self._model._addChannel()

        # start pipeline
        stringPipeline = "videotestsrc"
        _bin = Gst.parse_bin_from_description(stringPipeline, True)
        pipeline.add(_bin)
        pipeline.add(gtksink)
        # Link the pipeline to the sink that will display the video.
        _bin.link(gtksink)
        pipeline.set_state(Gst.State.PLAYING)

    def _startVideo(self,button):
        print("starting video")










class myView(Gtk.Window):
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    def __init__(self, **kw):
        super(myView, self).__init__(default_width=200, default_height=200, **kw)
        #self.window = Gtk.ApplicationWindow()
        self.hbox = Gtk.HBox()
        self.add(self.hbox)



        # self.window.connect('destroy', on_destroy)

        self._setup()
        self._update()

    def _setup(self):
        button_addChannel = Gtk.Button("Add channel")
        button_addChannel.connect("clicked", self._button_addChannel_pressed)
        self.hbox.add(button_addChannel)

    def _update(self):
        self.show_all()

    def _button_addChannel_pressed(self,obj):
        print("VIEW: button-addChannel-pressed")
        self.emit('button-addChannel-clicked')

    def _button_startChannel_pressed(self,obj):
        print("VIEW: button-startChannel-pressed")
        self.emit('button-startChannel-clicked')



    def _addVideoView(self,gtksink):
        #print(obj)
        #print(type(obj))
        print("add video")
        #widget = GstWidget('videotestsrc pattern=1')



        widget = GstWidget(gtksink)
        
        widget.set_size_request(200, 200)
        vbox = Gtk.VBox()
        vbox.add(widget)
        button_start = Gtk.Button("Start")
        button_start.connect("clicked", self._button_startChannel_pressed)
        vbox.add(button_start)

        self.hbox.add(vbox)

        #self.window.show_all()
        self._update()

class myModel:
    @property
    def greetee(self):
        return 'World'

    def __init__(self):
        self._channels = []

    def _addChannel(self):
        pass





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