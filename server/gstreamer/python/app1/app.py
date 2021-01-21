#https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gst
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
        self.view = view

    def addVideo(self):
        self.view.addVideo()



class myView:
    def __init__(self):
        self.window = Gtk.ApplicationWindow()
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)
        def on_destroy(win):
            Gtk.main_quit()

        self.window.connect('destroy', on_destroy)

        self.setup()
        self.update()

    def setup(self):
        button = Gtk.Button("Start")
        button.connect("clicked", self.addVideo)
        self.vbox.add(button)

    def update(self):
        self.window.show_all()


    def addVideo(self,obj):
        print(obj)
        print(type(obj))
        print("add video")
        #widget = GstWidget('videotestsrc pattern=1')

        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')

        widget = GstWidget(gtksink)
        
        widget.set_size_request(200, 200)

        self.vbox.add(widget)
        button = Gtk.Button("Start")
        self.vbox.add(button)

        self.window.show_all()

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