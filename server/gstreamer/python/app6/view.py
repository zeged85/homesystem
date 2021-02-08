import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject



class Handler:
    def __init__(self,view, channelNumber, builder):
        self.view = view
        self.channelNumber = channelNumber
        self.builder = builder

    def onDestroy(self, *args):
        print("view destroy")
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")
        self.view.emit("button-addChannel-clicked")

    def on_inputBox_changed(self, box):
        source = box.get_active_text()
        print(f"channel {self.channelNumber} input changed to {source}")
        self.view.emit('combobox-input-changed', int(self.channelNumber), str(source))

    def on_playButton_clicked(self, button):
        arg = self.channelNumber
        print("VIEW: button-startChannel-pressed", arg)
        self.view.emit('button-startChannel-clicked', int(arg))

    def on_stopButton_clicked(self, button):
        arg = self.channelNumber
        print("VIEW: button-stopChannel-pressed", arg)
        self.view.emit('button-stopChannel-clicked', int(arg))

    def on_addClient_clicked(self, button):
        # get ip, port fields and client list
        parent = button.get_parent()
        # print(parent)
        ipWidget = self.builder.get_object("sinkIP")
        portWidget = self.builder.get_object("sinkPort")
        ip = ipWidget.get_text()
        port = portWidget.get_text()
        print(ip, port)

        # check ip
        import socket
        try:
            if ip != "localhost":
                socket.inet_aton(ip)
            # legal
            print('legal ip')
        except socket.error:
            # Not legal
            print('invalid ip')
            return

        # check port

        try:
            intPort = int(port)
            if intPort < 0 or intPort > 65536:
                assert()
        except Exception as e:
            print('invalid port')
            return
        
        clientList = self.builder.get_object("clientList")

        row1 = Gtk.ListBoxRow()
        label1 = Gtk.Label(f"{ip}:{port}")
        row1.add(label1)

        clientList.add(row1)

        self.view._update()

       
        self.view.emit('button-addClient-clicked', int(self.channelNumber), ip, port)

        



    def cameraSourceSelected():
        pass

    def rtspSourceSelected():
        pass

    def testSourceSelected():
        pass

    def localSourceSelected():
        pass

    def captureSourceSelected():
        pass

    def youtubeSourceSelected():
        pass



class myView(Gtk.Window):
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'button-stopChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'combobox-input-changed': (GObject.SignalFlags.RUN_FIRST, None, (int, str,)),
        'button-addClient-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int, str, str,))
    }
    def __init__(self, **kw):
        super(myView, self).__init__(
            default_width=100, default_height=100, **kw)

        self._channels = {}
        self.channelNumber = 0
        

        self._inputs = ["test-src", "local file", "DVB",
            "Screen Capture", "USB-Camera", "youtube", "torrent",
            "UDP", "TCP", "RTSP", "Audio"]
        self._outputs = ["multi UDP sink"]

        self._attributes = ["file path","ip","port","cameras","protocol","pattern","uri"]


        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(Handler(self, self.channelNumber, self.builder))
  
        self.window = self.builder.get_object("window")



        self.channelsBox = self.builder.get_object("channelsBox")


    



        # self.setInputBox(self.builder)
        # self.setOutputBox(self.builder)


        '''
        #### list
        lst = self.builder.get_object("sinkList")

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
        '''

        # window.show_all()
        self._update()


        # self._hideAttributes()


    def _update(self):
        self.window.show_all()

    def _hideAttributes(self):

        cameraList = self.builder.get_object("cameraList")
        sourcePort = self.builder.get_object("sourcePort")

        cameraList.hide()
        sourcePort.hide()

    ### input
    def setInputBox(self, builder):
        combobox = builder.get_object("inputBox")
        for i in range(len(self._inputs)):
            combobox.append(None,str(self._inputs[i]))

    def setOutputBox(self, builder):
        combobox = builder.get_object("outputBox")
        for i in range(len(self._outputs)):
            combobox.append(None,str(self._outputs[i]))




    # add a new gst channel
    def _addVideoView(self, channelNum):
        tBuilder = Gtk.Builder()
        tBuilder.add_from_file("channelView.glade")
        
        # self.channelNumber += 1
        
        tBuilder.connect_signals(Handler(self, channelNum, tBuilder))

        tChannelBox = tBuilder.get_object("channelBox")
        # remove from old container TODO fix
        tChannelsBox = tBuilder.get_object("window")
        tChannelsBox.remove(tChannelBox)

        video_box = tBuilder.get_object("videoBox")

        self._channels[channelNum] = {
            'video_box': video_box
        }

        self.channelsBox.add(tChannelBox)

        self.setInputBox(tBuilder)
        self.setOutputBox(tBuilder)

        # hide attributes
        tPort = tBuilder.get_object("sourcePort")
        


        # Gtk.main()

        # print(lst.get_selected_row())

    def _setVideoView(self,gtksink, channelNum):
        video_box = self._channels.get(channelNum)['video_box']
        children = video_box.get_children ()
        for element in children:
            video_box.remove (element)

        video_widget = gtksink.get_property("widget")
        video_widget.set_size_request(200, 200)
        video_box.add(video_widget)
        self._update()
