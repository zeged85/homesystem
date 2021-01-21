#!/usr/bin/env python
import socket


class shell:
    def __init__(self, serverSocket):
        self.serverSocket = serverSocket


    

    def start_shell(self):
        while True:
            cmd = input('server>')

            #if cmd == 'list':
            #    self.serverSocket.sendall(b'list')
#
            #elif 'echo' in cmd:
            #    self.echo_message(cmd)
#
            ## TODO: add 'select all' feature   
            #elif 'select' in cmd:
            #    conn = self.get_target(cmd)
            #    if conn is not None:
            #        self.send_target_command(conn)
#
            #elif 'ping' in cmd:
            #    pass

            if cmd == '':
                continue
            else:
                self.serverSocket.sendall(bytes(cmd,"utf-8"))    

    def echo_message(self,cmd):
        action = cmd.replace('echo ', '')
        self.serverSocket.sendall(str.encode(action+"\n"))

   

    def wait_for_message(self):
        print("terminal waiting for ping reply")
        data = self.serverSocket.recv(2048)
        print("terminal recvd msg")
        print(data)
        #jsonObj = json.loads(data)

        #print(jsonObj)


        # Selecting the target
    def get_target(self,cmd):
        try:
            target = cmd.replace('select ', '') # target = id
            target = int(target) # cast to int
            conn = inputs[target]
            print("you are now connected to " + str(inputs[target].getpeername()[0]))
            print(str(inputs[target].getpeername()[0]) +":"+ str(inputs[target].getpeername()[1]) + ">", end="") # format prompt

            return conn

            # 192.168.0.4>

        except:
            print("Selection not valid")
            return None


    # Sends commands to client 
    def send_target_command(self,conn):
        while True:
            try:
                cmd = input()
                if cmd == 'quit':
                    #conn.close()
                    #s.close()
                    #sys.exit()
                    break
                if len(str.encode(cmd)) > 0:
                    #print(cmd)
                    #hello_msg = "what's up??\n"
                    #conn.sendall(hello_msg.encode())


                    msg = cmd+"\n"
                    #send_message(conn, msg)
                    #conn.sendall(msg)



                    #str.encode(cmd+"\n")
                    message_queues[conn].put(str.encode("test\n"))
                    if conn not in outputs:
                        outputs.append(conn)




                    #client_response = str(conn.recv(20480),"utf-8")
                    #print(client_response, end="")
            except:
                print("Bad command or file name")
                break

