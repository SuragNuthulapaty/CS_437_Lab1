import socket
import threading
import json
import move_non_block
import Ultrasonic
import sys
import time
import numpy as np
from picamera2 import Picamera2, MappedArray
import pickle
import struct
from io import BytesIO
import base64

ult = Ultrasonic.Ultrasonic()
mov = move_non_block.Move()
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

PORT = 65432

def capture_frame():
    image = picam2.capture_image()
    byte_io = BytesIO()
    image.save(byte_io, format="JPEG")
    return base64.b64encode(byte_io.getvalue()).decode("utf-8")

def handle_client(client, client_info):
    print(f"Connected to {client_info}")
    start_time = 0

    currently_moving = False

    try:
        while True:
            try:
                data = client.recv(1024)
            except BlockingIOError:
                data = None

            if currently_moving and time.time() - start_time > sleep_time:
                mov.stop()
                currently_moving = False

            if data:
                print(f"Client {client_info} disconnected.")
        
                str_val = data.decode().strip()
                print(f"Received: {str_val}")

                if not currently_moving:
                    if str_val == "l":
                        sleep_time = mov.left()
                        currently_moving = True
                    elif str_val == "r":
                        sleep_time = mov.right()
                        currently_moving = True
                    elif str_val == "f":
                        sleep_time = mov.forward()
                        currently_moving = True
                    elif str_val == "b":
                        sleep_time = mov.back()
                        currently_moving = True
                    
                    start_time = time.time()

            print("sending")
            
            frame = capture_frame()

            sensor_data = {
                "distance": ult.get_distance(),
                "direction": 1 if currently_moving else 0,
                "img": frame
            }

            json_data = json.dumps(sensor_data)
            client.sendall(json_data.encode())

            time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def start_server(host):
    """Starts the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, PORT))
        server_socket.listen()

        print(f"Server listening on port {PORT}")

        try:
            while True:
                client, client_info = server_socket.accept()
                client.setblocking(False)
                client_thread = threading.Thread(target=handle_client, args=(client, client_info), daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        hostname = "0.0.0.0"
    else:
        hostname = sys.argv[1]

    start_server(hostname)
