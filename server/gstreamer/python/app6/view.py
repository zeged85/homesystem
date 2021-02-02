import gi
from gi.repository import Gtk, GObject

gi.require_version("Gtk", "3.0")


class Handler:
    def __init__(self,view):
        self.view = view

    def onDestroy(self, *args):
        print("view destroy")
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")
        self.view.emit("button-addChannel-clicked")


class myView(Gtk.Window):
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    def __init__(self, **kw):
        super(myView, self).__init__(
            default_width=100, default_height=100, **kw)
        builder = Gtk.Builder()
        builder.add_from_file("channelView.glade")
        builder.connect_signals(Handler(self))


        window = builder.get_object("window")
        lst = builder.get_object("list1")

        row1 = Gtk.ListBoxRow()
        label1 = Gtk.Label("test-1")
        row1.add(label1)

        row2 = Gtk.ListBoxRow()
        label2 = Gtk.Label("test-2")
        row2.add(label2)

        row3 = Gtk.ListBoxRow()
        label3 = Gtk.Label("test-3")
        row3.add(label3)



        lst.add(row1)
        lst.add(row2)
        lst.add(row3)
        window.show_all()


        # Gtk.main()

        # print(lst.get_selected_row())
