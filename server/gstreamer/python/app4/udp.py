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
        bus = pipeline.get_bus()
        # bus.add_signal_watch()
        bus.enable_sync_message_emission()
        factory = pipeline.get_factory()
        # gtksink = factory.make('gtksink')

        # p = Gst.parse_launch("v4l2src ! videoconvert ! gtksink name=sink")                                             
        # p = Gst.parse_launch("videotestsrc ! videoconvert ! gtksink name=sink") 
        stringPipeline = """udpsrc uri=udp://localhost:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! queue name=convert ! gtksink name=sink"""                                            
        p = Gst.parse_launch(stringPipeline) 
        s = p.get_by_name("sink")
        # box.pack_start(s.props.widget, ...)

        # pipeline.add(self._bin)
        pipeline.add(p)
        # pipeline.add(s)
        # Link the pipeline to the sink that will display the video.
        # self._bin.link(s)
        self.pack_start(s.props.widget, True, True, 0)
        s.props.widget.show()
        # Start the video
        pipeline.set_state(Gst.State.PLAYING)


window = Gtk.ApplicationWindow()

# Create a gstreamer pipeline with no sink. 
# A sink will be created inside the GstWidget.
stringPipeline = """udpsrc uri=udp://localhost:5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! queue name=convert"""
# widget = GstWidget(stringPipeline)
widget = GstWidget('videotestsrc')
widget.set_size_request(200, 200)

window.add(widget)

window.show_all()


def on_destroy(win):
    Gtk.main_quit()

window.connect('destroy', on_destroy)

Gtk.main()