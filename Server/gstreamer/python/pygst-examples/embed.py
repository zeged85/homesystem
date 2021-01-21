#https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gst
Gst.init(None)
Gst.init_check(None)


class GstWidget(Gtk.Box):
    def __init__(self, pipeline):
        super().__init__()
        # Only setup the widget after the window is shown.
        self.connect('realize', self._on_realize)

        # Parse a gstreamer pipeline and create it.
        self._bin = Gst.parse_bin_from_description(pipeline, True)

    def _on_realize(self, widget):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        pipeline.add(self._bin)
        pipeline.add(gtksink)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(gtksink)
        self.pack_start(gtksink.props.widget, True, True, 0)
        gtksink.props.widget.show()
        # Start the video
        pipeline.set_state(Gst.State.PLAYING)


window = Gtk.ApplicationWindow()

vbox = Gtk.VBox()
window.add(vbox)

# Create a gstreamer pipeline with no sink. 
# A sink will be created inside the GstWidget.
widget = GstWidget('videotestsrc')
widget.set_size_request(200, 200)

vbox.add(widget)
button = Gtk.Button("Start")
vbox.add(button)

window.show_all()


def on_destroy(win):
    Gtk.main_quit()

window.connect('destroy', on_destroy)

Gtk.main()