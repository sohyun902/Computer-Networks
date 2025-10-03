# Computer-Networks

## Project Structure

- **client/Client.py**
The client program. Handles user authentication, service selection (text calculator, image, video streaming, etc.), and communication with the server.

- **local/Local.py**
Local server. Manages client authentication, provides image/video/text services, and forwards certain requests to the global server if needed.

- **global/Global.py**
Global server. Provides text calculation, image delivery, and video_2022.mp4 streaming services.

- **local/ID_authen_binary.txt**
A list of allowed client IDs in binary format.

- **local/videos/, global/videos/**
Directories for storing video files.

- **local/Image.jpg, global/Image.jpg**
Image files used for the image service.

## Features

- **Client Authentication**:
  - Clients verify their ID (last 5 digits of student ID) with the local server.
  - Maximum 3 attempts allowed; connection terminated upon failure.

- **Text Service (Calculator)**:
  - Clients can send arithmetic expressions to the server.
  - Server evaluates expressions and returns the result.

- **Image Service**:
  - Local server delivers cached images to clients.

- **Video Service**:
  - **video_2023**: Cached in local server; sent with audio to clients.
  - **video_2022**: Not cached locally; fetched from global server, stored locally, then delivered to clients.
  - Supports frame-by-frame streaming and audio playback using OpenCV and PyAudio.

- **Caching Mechanism**:
  - Local server caches text, image, and video_2023 for faster client responses.
  - Uncached resources are retrieved from global server when requested.
 
## Services

- **Text**  
  The client sends a mathematical expression, and the server evaluates it and returns the result.

- **Image**  
The client receives a stored image from the server and displays it on the screen.

- **video_2022 / video_2023**  
  The client receives stored video frames from the server and plays both video and audio synchronously.

- **Exit**  
  Terminates the connection

## Authentication

- The client enters a numeric ID.
- The server converts the ID to a binary string and checks whether it exists in ID_authen_binary.txt.
- If verification fails three times, the connection is terminated.

## Video Files Download

The project uses two video files which are too large for GitHub:

- [Download video_2022.mp4](https://drive.google.com/file/d/1wlcRem1iaPVTBbtuMB-o71LSnkYTbG7c/view?usp=drive_link).
- [Download video_2023.mp4](https://drive.google.com/file/d/1UInVEF4Itl-4A7HnWEIvYPaPTOlTBzmQ/view?usp=drive_link)
