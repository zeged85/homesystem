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


class myController:
    def __init__(self,view):
        self._view = view
        self._view.connect('button1-clicked', self._addVideo)
        self._view.connect('destroy', self.on_destroy)

    def _addVideo(self, button):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        self._view._addVideo(gtksink)

    def on_destroy(self, win):
        Gtk.main_quit()



class myView(Gtk.Window):
    __gsignals__ = {
        'button1-clicked': (GObject.SignalFlags.RUN_FIRST, None, ())
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
        button = Gtk.Button("Add channel")
        button.connect("clicked", self._button1pressed)
        self.hbox.add(button)

    def _update(self):
        self.show_all()

    def _button1pressed(self,obj):
        print("VIEW: button1pressed")
        self.emit('button1-clicked')



    def _addVideo(self,gtksink):
        #print(obj)
        #print(type(obj))
        print("add video")
        #widget = GstWidget('videotestsrc pattern=1')



        widget = GstWidget(gtksink)
        
        widget.set_size_request(200, 200)
        vbox = Gtk.VBox()
        vbox.add(widget)
        button = Gtk.Button("Start")
        vbox.add(button)

        self.hbox.add(vbox)

        #self.window.show_all()
        self._update()

class myModel:
    def __init__(self):
        pass



if __name__ == "__main__":
        

    # window = Gtk.ApplicationWindow()

    view = myView()


    # vbox = Gtk.VBox()

    # window
    # window.add(vbox)

    # model
    controller = myController(view)

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