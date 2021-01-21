#!/usr/bin/env python
import gi
gi.require_version("Gst", "1.0")
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk
from gstPipeline import GTK_Main

# GObject.threads_init() # yGIDeprecationWarning: Since version 3.11, calling threads_init is no longer needed. See: https://wiki.gnome.org/PyGObject/Threading
# TODO: remove import GObject

# self.set_icon_from_file("web.png")
Gst.init(None)        
g =  GTK_Main()
g.player.set_state(Gst.State.PLAYING)
Gtk.main()