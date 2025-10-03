# Import libraries
from socket import *
import os
import threading

def handle(client_socket):
    # Receive request from the client
    service=client_socket.recv(4096).decode('utf-8')

    # When the client selects Text service
    if service=="Text":
        ask_exp="Type your expression: "
        client_socket.send(ask_exp.encode('utf-8'))

        # Receive expression from client
        exp=client_socket.recv(4096).decode('utf-8')
        # Send the answer about the expression to the client
        answer=str(eval(exp))
        client_socket.send(answer.encode('utf-8'))

    # When the client selects Image service
    if service=="Image":
        # Read Image file and send it to the client
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "Image.jpg")
        with open(image_path, "rb") as f:
            while True:
                data=f.read(4096)
                if not data:
                    print("END")
                    client_socket.send("END".encode('utf-8'))
                    break
                client_socket.send(data)
        # Receive a message that the client successfully received
        client_socket.recv(4096).decode('utf-8')

    # When the client selects video_2022 service
    if service=="video_2022":
        # Read video_2022.mp4 file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, "videos", "video_2022.mp4")
        # Send the video with audio to the client 
        with open(filename, 'rb') as f:
            while True:
                bytes_read=f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        client_socket.close()

# Define the server name and port number
host='127.0.0.1'
port=9000

#Create the server socket
server_socket=socket(AF_INET, SOCK_STREAM)

# Bind the socket to our local address
server_socket.bind((host, port))
server_socket.listen()

print("Listening at", (host, port))

# Multithreading for multiple clients
while True:
    client_socket, client_address=server_socket.accept()
    print(client_address)
    client_handler=threading.Thread(target=handle, args=(client_socket, ))
    client_handler.start()
