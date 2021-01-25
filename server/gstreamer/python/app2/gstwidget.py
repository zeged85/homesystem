from gi.repository import Gtk  # , Gst  # ,GObject
import gi
gi.require_version('Gtk', '3.0')


class GstWidget(Gtk.Box):
    def __init__(self, gtksink):
        super().__init__()
        # Only setup the widget after the window is shown.
        self.connect('realize', self._on_realize)
        self.gtksink = gtksink

    def _on_realize(self, widget):
        self.pack_start(self.gtksink.props.widget, True, True, 0)
        self.gtksink.props.widget.show()
