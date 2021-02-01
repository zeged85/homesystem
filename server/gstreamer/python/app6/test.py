import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


builder = Gtk.Builder()
builder.add_from_file("channelView.glade")
# builder.connect_signals(Handler())

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

Gtk.main()

import time
while True:
    print(lst.get_selected_row())
    time.sleep(1)