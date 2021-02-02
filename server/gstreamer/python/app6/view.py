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

    def on_inputBox_changed(self, box):
        print("input changed")
        # print(box.get_selected_row())
        print(box.get_active_text())

class MainControllsHandler:
    def on_addChannel_clicked(self, button):
        print("add channel")


class myView(Gtk.Window):
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    def __init__(self, **kw):
        super(myView, self).__init__(
            default_width=100, default_height=100, **kw)
        

        
        builder = Gtk.Builder()
        builder.add_from_file("channelView2.glade")
        builder.connect_signals(Handler(self))
  
        window = builder.get_object("window")



        self.channelsBox = builder.get_object("channelsBox")



        ### input
        combobox = builder.get_object("inputBox")

        _inputs = [
            ["Select input"], ["test-src"], ["local file"], ["DVB"],
            ["Screen Capture"], ["USB-Camera"], ["youtube"], ["torrent"],
            ["UDP"], ["TCP"], ["RTSP"], ["Audio"]]
        # listmodel = Gtk.ListStore(str)
        # append the data in the model
        for i in range(len(_inputs)):
            # listmodel.append(self._inputs[i])
            combobox.append(None,str(_inputs[i]))
            print(combobox.get_active_text())


        #### list
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


    def _addVideoView(self):
        tBuilder = Gtk.Builder()
        tBuilder.add_from_file("channelView2.glade")
        tBuilder.connect_signals(Handler(self))

        tChannelsBox = tBuilder.get_object("channelsBox")
        tChannelBox = tBuilder.get_object("channelBox")
        tChannelsBox.remove(tChannelBox)

        self.channelsBox.add(tChannelBox)


        # Gtk.main()

        # print(lst.get_selected_row())
