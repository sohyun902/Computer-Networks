# Import libraries
from socket import *
import cv2
import pickle
import struct
import threading
import os
import ffmpeg

def handle(client_socket):
    # Verify the received client ID
    base_dir = os.path.dirname(os.path.abspath(__file__))
    id_file_path = os.path.join(base_dir, "ID_authen_binary.txt")
    f = open(id_file_path, "r")
    ID_authen=f.read()
    ID_list=ID_authen.split("\n")

    found=False
    for i in range(3):
        request="Enter the client ID: "
        client_socket.send(request.encode('utf-8'))

        id_5=client_socket.recv(4096).decode('utf-8')

        if id_5.isdigit()==False:
            continue

        id_5=bin(int(id_5))[2:]

        for id in ID_list:
            if int(id_5)==int(id):
                found=True
                break
        # Verification success case
        if found:
            client_socket.send("SUCCESS".encode('utf-8'))
            break

    # Verification failed case
    if not found:
        client_socket.send("FAILED".encode('utf-8'))
        client_socket.close()
        return
        
    while True:
        ask="Choose service you are looking for: "
        client_socket.send(ask.encode('utf-8'))

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
            image_path = os.path.join(base_dir, "Image.jpg")
            with open(image_path, "rb") as f:
                while True:
                    data=f.read(4096)
                    if not data:
                        client_socket.send("END".encode('utf-8'))
                        break
                    client_socket.send(data)
            
            # Receive a message that the client successfully received
            client_socket.recv(4096).decode('utf-8')

        # When the client selects video_2022 service
        if service=="video_2022":
            # Send the request to the Global server
            connect_socket=socket(AF_INET, SOCK_STREAM)
            connect_socket.connect((host, global_port))
            connect_socket.send(service.encode('utf-8'))

            # Save the received video 
            video_path = os.path.join(base_dir, "videos", "video_2022.mp4")
            with open(video_path, 'wb') as f:
                while True:
                    bytes_read=connect_socket.recv(4096)
                    
                    if not bytes_read:
                        break
                    f.write(bytes_read)

            # Send the received video with audio to the client
            video=cv2.VideoCapture(video_path)
            # Extract audio from the video
            process=(ffmpeg.input(video_path).output('pipe:', format='wav').run_async(pipe_stdout=True, pipe_stderr=True))
            while True:
                # Service stop case
                if client_socket.recv(4096).decode('utf-8')=="STOP":
                    break
                # Read frame and audio
                _, frame=video.read()
                if not _:
                    client_socket.send("END".encode('utf-8'))
                    break

                audio=process.stdout.read(4096)
                frame=cv2.resize(frame, (400, 200))

                # Serialize the frame and audio data
                a=pickle.dumps(frame)
                b=pickle.dumps(audio)

                # Send them to the client
                msg=struct.pack("Q", len(a))+a+struct.pack("Q", len(b))+b
                client_socket.sendall(msg)

        # When the client selects video_2023 service
        if service=="video_2023":
            # Read video_2023.mp4 file
            filename=os.path.join(base_dir, "videos", "video_2023.mp4")
            # path of the file was copied, so it is recommended to modify the path 
            
            video=cv2.VideoCapture(filename)
            # Extract audio from the video
            process=(ffmpeg.input(filename).output('pipe:', format='wav').run_async(pipe_stdout=True, pipe_stderr=True))

            while True:
                # Service stop case
                if client_socket.recv(4096).decode('utf-8')=="STOP":
                    break
                # Read frame and audio
                _, frame=video.read()
                if not _:
                    client_socket.send("END".encode('utf-8'))
                    break
                
                audio=process.stdout.read(4096)
                frame = cv2.resize(frame, (400, 200))

                # Serialize the frame and audio data
                a=pickle.dumps(frame)
                b=pickle.dumps(audio)

                # Send them to the client
                msg=struct.pack("Q", len(a))+a+struct.pack("Q", len(b))+b
                client_socket.sendall(msg)
      
        # When the client wants to exit
        if service=='Exit':
            # Close the connection
            client_socket.close()
            return   

#Define the server name and port number
host='127.0.0.1'
local_port=8000
global_port=9000

#Create the server socket
server_socket=socket(AF_INET, SOCK_STREAM)

# Bind the socket to our local address
server_socket.bind((host, local_port))
server_socket.listen()

print("Listening at", (host, local_port))

# Multithreading for multiple clients
while True:
    client_socket, client_address=server_socket.accept()
    print(client_address)
    client_handler=threading.Thread(target=handle, args=(client_socket, ))
    client_handler.start()
