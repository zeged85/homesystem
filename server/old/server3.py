import socket,os
from threading import Thread

class socketListener(Thread):
    def run(self):
        soc = socket.socket(socket.AF_INET)
        soc.bind(('localhost',8000))
        soc.listen(0)
        client = soc.accept()

pid = os.getpid()
sl = socketListener()
sl.start()
input('Socket is listening, press any key to abort...')
os.kill(pid,9)