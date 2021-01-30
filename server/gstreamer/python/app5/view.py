from gi.repository import Gtk, GObject  # , Gst
import gi
# from gstwidget import GstWidget

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')


class PathField():
    def __init__(self):
        pass


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
            default_width=100, default_height=100, **kw)
        # self.window = Gtk.ApplicationWindow()
        self._channels = {}
        self.channelNumber = 0
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
                "You chose " + inputType + ".")
            self.emit(
                'combobox-input-changed', int(channelNum), str(inputType))
            # if inputType == "youtube":
            #     self._addPathField(channelNum)
        else:
            print("channel input off")

        return True

    def _addPathField(self, channelNum):
        hbox_field = Gtk.HBox()
        field = Gtk.Entry()
        hbox_field.add(field)
        line = self._channels[channelNum]['vbox']
        # line.pack_start(hbox_field, True, True, 0)
        line.pack_end(hbox_field, True, True, 0)
        
        # line.add(hbox_field)
        self._update()  # refresh window
        
    def _createSourceField(Self):
        hbox_field = Gtk.HBox()
        field = Gtk.Entry()
        hbox_field.add(field)
        return hbox_field

    def _createTransportBar(self):
        # Start / Stop Buttons - transport layer
        hbox_transport = Gtk.HBox()
        # start
        button_start = Gtk.Button(label="Start")
        button_start.connect(
            "clicked", self._button_startChannel_pressed, self.channelNumber)
        hbox_transport.add(button_start)
        # stop
        button_stop = Gtk.Button(label="Stop")
        button_stop.connect(
            "clicked", self._button_stopChannel_pressed, self.channelNumber)
        hbox_transport.add(button_stop)
        return hbox_transport

    def _createSourceBox(self):
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
        combobox.connect("changed", self.on_changed, self.channelNumber)
        return combobox

    # def _createSourceField(self):

    def _setVideoView(self,gtksink, channelNum):
        video_box = self._channels.get(channelNum)['video_box']
        children = video_box.get_children ()
        for element in children:
            video_box.remove (element)

        video_widget = gtksink.get_property("widget")
        video_widget.set_size_request(200, 200)
        video_box.add(video_widget)
        self._update()

    def _addVideoView(self, gtksink):
        print("add video")
        # widget = GstWidget('videotestsrc pattern=1')
        # channelNumber = len(self._channels)

        # Video View
        # widget = GstWidget(gtksink)
        # widget.set_size_request(200, 200)
        vbox = Gtk.VBox()
        # vbox.add(widget)

        # drawingarea = Gtk.DrawingArea()
        video_box = Gtk.Box()
        video_box.set_size_request(200,200)
        # video_widget = gtksink.get_property("widget")
        # video_widget.set_size_request(200, 200)
        # video_box.add(video_widget)
        vbox.add(video_box)

        hbox_transport = self._createTransportBar()
        vbox.add(hbox_transport)
        
        # add the combobox to the window
        combobox = self._createSourceBox()
        vbox.add(combobox)
        sourceField = self._createSourceField()
        vbox.add(sourceField)
        self.hbox.add(vbox)

        self._channels[self.channelNumber] = {
            'vbox': vbox,
            'video_box': video_box
        }
        self.channelNumber += 1
        # self.window.show_all()
        self._update()
