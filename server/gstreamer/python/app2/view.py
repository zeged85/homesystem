from gi.repository import Gtk, GObject  # , Gst
import gi
from gstwidget import GstWidget

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


class myView(Gtk.Window):
    # https://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html
    # emit w/ args
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'button-stopChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'combobox-input-changed': (GObject.SignalFlags.RUN_FIRST, None, (int, str,))
    }

    def __init__(self, **kw):
        super(myView, self).__init__(
            default_width=200, default_height=200, **kw)
        # self.window = Gtk.ApplicationWindow()
        self._channels = -1
        self.hbox = Gtk.HBox()
        self.add(self.hbox)
        # TODO: popUP - for local file browser
        self._inputs = [
            ["Select input"], ["test-src"], ["local file"], ["DVB"],
            ["Screen Capture"], ["USB-Camera"], ["youtube"], ["torrent"],
            ["UDP"], ["TCP"], ["RTSP"], ["Audio"]]

        # self.window.connect('destroy', on_destroy)

        self._setup()
        self._update()

    def _setup(self):
        button_addChannel = Gtk.Button(label="Add channel")
        button_addChannel.connect("clicked", self._button_addChannel_pressed)
        self.hbox.add(button_addChannel)

    def _update(self):
        self.show_all()

    def _button_addChannel_pressed(self, obj):
        print("VIEW: button-addChannel-pressed")
        self.emit('button-addChannel-clicked')

    def _button_startChannel_pressed(self, obj, arg):
        print("VIEW: button-startChannel-pressed", arg)
        self.emit('button-startChannel-clicked', int(arg))

    def _button_stopChannel_pressed(self, obj, arg):
        print("VIEW: button-stopChannel-pressed", arg)
        self.emit('button-stopChannel-clicked', int(arg))

    def on_changed(self, combo, channelNum):
        # if the row selected is not the first one, write its value on the
        # terminal
        if combo.get_active() != 0:
            inputType = str(self._inputs[combo.get_active()][0])
            print(
                "You chose " + str(self._inputs[combo.get_active()][0]) + ".")
            self.emit(
                'combobox-input-changed', int(channelNum), str(inputType))

        return True

    def _addVideoView(self, gtksink):
        print("add video")
        # widget = GstWidget('videotestsrc pattern=1')
        self._channels += 1
        channelNumber = self._channels

        # Video View
        widget = GstWidget(gtksink)
        widget.set_size_request(200, 200)
        vbox = Gtk.VBox()
        vbox.add(widget)

        # Start / Stop Buttons - transport layer
        hbox_transport = Gtk.HBox()
        # start
        button_start = Gtk.Button(label="Start")
        button_start.connect(
            "clicked", self._button_startChannel_pressed, channelNumber)
        hbox_transport.add(button_start)
        # stop
        button_stop = Gtk.Button(label="Stop")
        button_stop.connect(
            "clicked", self._button_stopChannel_pressed, channelNumber)
        hbox_transport.add(button_stop)

        vbox.add(hbox_transport)
        # ComboBox
        # TODO: move to own class

        listmodel = Gtk.ListStore(str)
        # append the data in the model
        for i in range(len(self._inputs)):
            listmodel.append(self._inputs[i])

        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) 
        # to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(0)

        # connect the signal emitted when a row is selected to the callback
        # function
        combobox.connect("changed", self.on_changed, channelNumber)

        # add the combobox to the window
        vbox.add(combobox)

        self.hbox.add(vbox)

        # self.window.show_all()
        self._update()
