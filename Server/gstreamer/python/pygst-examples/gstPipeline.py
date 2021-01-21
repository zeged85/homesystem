
#!/usr/bin/env python

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GTK_Main:
    
    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Videotestsrc-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        #button start/stop
        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)

        #button dynamic change
        self.buttonDyn = Gtk.Button("change")
        self.buttonDyn.connect("clicked", self.dyn)
        self.pattern = 0
        vbox.add(self.buttonDyn)
        window.show_all()
        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("videotestsrc", "video-source")
        clock = Gst.ElementFactory.make("clockoverlay", "clock-effect")
        sink = Gst.ElementFactory.make("xvimagesink", "video-output")
        caps = Gst.Caps.from_string("video/x-raw, width=320, height=230")
        filter = Gst.ElementFactory.make("capsfilter", "filter")
        filter.set_property("caps", caps)
        self.player.add(source)
        self.player.add(filter)
        self.player.add(clock)
        self.player.add(sink)
        source.link(filter)
        filter.link(clock)
        clock.link(sink)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            #self.player.get_by_name("video-source").set_property("pattern", 1)

    def dyn(self, w):
        self.pattern+=1
        self.player.get_by_name("video-source").set_property("pattern", self.pattern)
        print(self.pattern)
        if (self.pattern==24):
            self.pattern=-1

if __name__ == "__main__":
    GObject.threads_init()
    Gst.init(None)        
    GTK_Main()
    Gtk.main()
