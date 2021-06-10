import socket, threading    
from tkinter import *
import subprocess as sp
from authentication import fingerprintAuth       #Libraries import


#Choosing unreserved port
host = '127.0.0.1'                                                      #LocalHost
port = 8088        


# initialization
# root = Tk()
# root.title("Myot")
# root.geometry('750x400')
# root.mainloop()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()


clients = []
nicknames = [1]
uhidNum = ''
temperature = ''
oxygenLevel= ''
heartBeat= ''
age= 37


def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)


def handle(client,nickname):                                         
    while True:
       
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            print(nickname)

            if  message:
 
                if nickname== "Sensor1":
                    print("Fingerprint Sensor Activation Finished")
                    fingerprintAuth(message.decode('ascii'))
                    client.send('DataFetched'.encode('ascii'))
                    client.close()

                elif nickname=='Sensor2':
                    print("Temperature Sensor Activation Finished")
                    client.send('Temperature Fetched'.encode('ascii'))
                    client.close()

                elif nickname=='Sensor3':
                    print("Oximeter Sensor Activation Finished")
                    client.close()

                elif age>30:
                    if nickname=="Cam1":
                        print("Fundus Camera Activation Finished")

            else:
               print("Place Fingerprint / Aadhar Card infront of scanner")
       
            # broadcast(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():                                                          #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('Sensor'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        
        clients.append(client)
        print("Activated Sensor is {}".format(nickname))
        broadcast("{} joined!\n".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,nickname))
        thread.start()

receive()


