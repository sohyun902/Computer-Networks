# Import libraries
from socket import *
import cv2
import pickle
import struct
import numpy as np
import pyaudio

# Define the address and port number
host='127.0.0.1'
port=8000

# Create the client socket
client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))

#Get client ID from the user then send it to the server
while True:
    request=client_socket.recv(4096).decode('utf-8')
    if request=='SUCCESS':
        break
    if request=="FAILED":
        break
    id=input(request)
    client_socket.send(id.encode('utf-8'))
if request=="FAILED":
    print("Verification Failed!")
    exit()


while True:
    ask=client_socket.recv(4096)
    
    if 'x' in str(ask[:]):
        continue
    
    # Request service that the client wants to the server
    service=input(ask.decode('utf-8'))
    client_socket.send(service.encode('utf-8'))

    # When the client selects Text service
    if service=="Text":
        # Send expression to the server
        ask_exp=client_socket.recv(4096).decode('utf-8')
        exp=input(ask_exp)
        client_socket.send(exp.encode('utf-8'))

        # Receive answer from the server
        answer=client_socket.recv(4096).decode('utf-8')
        print(answer)

    # When the client selects Image service
    if service=="Image":
        img_data = b""
        while True:
            data = client_socket.recv(4096)
            if data == b"END":
                break
            img_data += data

        np_data = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to load image")
        else:
            cv2.imshow('Image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Send a message that the client received successfully
        client_socket.send("Received".encode('utf-8'))

    # When the client selects video_2022 service
    if service=="video_2022":

        audio=pyaudio.PyAudio()
        stream=audio.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True, frames_per_buffer=1024)
            
        # Generate empty byte string
        data=b""
        payload_size=struct.calcsize("Q")
        end=False

        # Receive data from the server and get the size of message
        while True:
            client_socket.send("CONTINUE".encode('utf-8'))
            while len(data)<payload_size:
                packet=client_socket.recv(4096)
                if not packet:
                    break
                # Service stop case
                if packet==b'END':
                    end=True
                    break
                data=data+packet
            
            if end:
                cv2.destroyAllWindows()
                break
            
            packed_msg_size=data[:payload_size]
            data=data[payload_size:]
            unpacked_msg_size=struct.unpack("Q", packed_msg_size)[0]

            # Receive the whole frame data
            while len(data)<unpacked_msg_size:
                data=data+client_socket.recv(4096)

            Frame=data[:unpacked_msg_size]
            data=data[unpacked_msg_size:]

            # Deserialize frame data
            frame=pickle.loads(Frame)

            while len(data)<payload_size:
                packet=client_socket.recv(4096)
                if not packet:
                    break
                data=data+packet
            
            packed_audio_size=data[:payload_size]
            data=data[payload_size:]
            unpacked_audio_size=struct.unpack("Q", packed_audio_size)[0]

            # Receive the whole audio data
            while len(data)<unpacked_audio_size:
                data=data+client_socket.recv(4096)

            Audio=data[:unpacked_audio_size]
            data=data[unpacked_audio_size:]

            # Deserialize audio data
            audio_frame=pickle.loads(Audio)

            # Display the frame and audio
            cv2.imshow("FROM CACHE SERVER", frame)
            stream.write(audio_frame)
            key=cv2.waitKey(1)
            
            if key==ord('q'):
                client_socket.send("STOP".encode('utf-8'))
                cv2.destroyAllWindows()
                break
       
    # When the client selects video_2022 service
    if service=="video_2023":

        audio=pyaudio.PyAudio()
        stream=audio.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True, frames_per_buffer=1024)
            
        # Generate empty byte string
        data=b""
        payload_size=struct.calcsize("Q")
        end=False

        # Receive data from the server and get the size of message
        while True:
            client_socket.send("CONTINUE".encode('utf-8'))
            while len(data)<payload_size:
                packet=client_socket.recv(4096)
                if not packet:
                    break
                # Service stop case
                if packet==b'END':
                    end=True
                    break
                data=data+packet
            
            if end:
                cv2.destroyAllWindows()
                break
            
            packed_msg_size=data[:payload_size]
            data=data[payload_size:]
            unpacked_msg_size=struct.unpack("Q", packed_msg_size)[0]

            # Receive the whole frame data
            while len(data)<unpacked_msg_size:
                data=data+client_socket.recv(4096)

            Frame=data[:unpacked_msg_size]
            data=data[unpacked_msg_size:]

            # Deserialize frame data
            frame=pickle.loads(Frame)

            while len(data)<payload_size:
                packet=client_socket.recv(4096)
                if not packet:
                    break
                data=data+packet
            
            packed_audio_size=data[:payload_size]
            data=data[payload_size:]
            unpacked_audio_size=struct.unpack("Q", packed_audio_size)[0]

            # Receive the whole audio data
            while len(data)<unpacked_audio_size:
                data=data+client_socket.recv(4096)

            Audio=data[:unpacked_audio_size]
            data=data[unpacked_audio_size:]

            # Deserialize audio data
            audio_frame=pickle.loads(Audio)

            # Display the frame and audio
            cv2.imshow("FROM CACHE SERVER", frame)
            stream.write(audio_frame)
            key=cv2.waitKey(1)
            
            if key==ord('q'):
                client_socket.send("STOP".encode('utf-8'))
                cv2.destroyAllWindows()
                break
    
    # When the client wants to exit
    if service=="Exit":
        client_socket.close()
        break               

                
                
        
        