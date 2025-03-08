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
from vidstream import startStreamingServer
import servo

ult = Ultrasonic.Ultrasonic()
mov = move_non_block.Move()
serv = servo.Servo()

serv.setServoPwm("1", 80)

PORT = 65432

def handle_client(client, client_info):
    print(f"Connected to {client_info}")
    currently_moving = False

    try:
        while True:
            try:
                data = client.recv(1024)
            except BlockingIOError:
                data = None

            if data:
                print(f"Client {client_info} disconnected.")

                str_val = data.decode().strip()
                print(f"Received: {str_val}")

                if "s" in str_val:
                    mov.stop()
                    currently_moving = False

                if str_val[0] == "l":
                    sleep_time = mov.left()
                    currently_moving = True
                elif str_val[0] == "r":
                    sleep_time = mov.right()
                    currently_moving = True
                elif str_val[0] == "f":
                    sleep_time = mov.forward()
                    currently_moving = True
                elif str_val[0] == "b":
                    sleep_time = mov.back()
                    currently_moving = True
                elif str_val[0] == "s":
                    mov.stop()
                    currently_moving = False
                elif str_val[0] == "0":
                    mov.stop()
                    currently_moving = False

                    v = int(str_val.split()[1])

                    while v > 150:
                        v //= 10

                    serv.setServoPwm('0', int(v))

                    print("0", int(v))
                        
                    # elif str_val[0] == "1":
                    #     mov.stop()
                    #     currently_moving = False

                    #     v = str_val.split()[1]

                    #     serv.setServoPwm('1', int(v))
                    #     print("1", v)

            sensor_data = {
                "distance": ult.get_distance(),
                "direction": 1 if currently_moving else 0
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

        # start video server
        video_thread = threading.Thread(target=startStreamingServer)
        video_thread.start()

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
        
        mov.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        hostname = "0.0.0.0"
    else:
        hostname = sys.argv[1]

    start_server(hostname)
