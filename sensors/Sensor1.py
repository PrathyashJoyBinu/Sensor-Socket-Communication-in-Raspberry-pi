import socket, threading
sensor = 'Sensor1'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 8088))   #connecting client to server



def receive():
    while True:                                                 #making valid connection
        try:
            recmessage = client.recv(8024).decode('ascii')
            
            if recmessage == 'Sensor':
                client.send(sensor.encode('ascii'))

            else:
                if recmessage == 'DataFetched':
                    
                    print("Sensor 1 Service Closed")


                else:
                    print(recmessage)

            
      
            
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break


def write():
    while True:                                                 #message layout
        message =  input('')
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write) #writing multiple messages                   #sending messages 
write_thread.start()