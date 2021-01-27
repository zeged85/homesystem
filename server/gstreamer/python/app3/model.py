from gstChannel import gstChannel
class myModel:
    @property
    def greetee(self):
        return 'World'

    def __init__(self):
        self._channels = []

    def _createChannel(self):
        print("model add (create) channel")

        channel = gstChannel()
        self._channels.append(channel)

        return (len(self._channels)-1)

    def _getGtksink(self, channelNum):
        return self._channels[channelNum].gtksink

    def _setTestsrc(self, channelNum):
        self._channels[channelNum]._setTestsrc()

    def _play(self, channelNum):
        self._channels[channelNum]._play()

    def _stop(self, channelNum):
        self._channels[channelNum]._stop()

    def _setInput(self, channelNum, inputType):
        self._channels[channelNum]._setInput(inputType)
