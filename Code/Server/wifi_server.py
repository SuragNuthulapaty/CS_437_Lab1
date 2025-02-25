import socket
import threading
import json
import move
import Ultrasonic

ult = Ultrasonic.Ultrasonic()
mov = move.Move()
PORT = 65432

def handle_client(client, client_info):
    """Handles communication with a connected client."""
    print(f"✅ Connected to {client_info}")
    try:
        while True:
            data = client.recv(1024)
            if not data:
                print(f"❌ Client {client_info} disconnected.")
                break
        
            str_val = data.decode().strip()
            print(f"Received: {str_val}")

            if str_val == "l":
                mov.left()
            elif str_val == "r":
                mov.right()
            elif str_val == "f":
                mov.forward()
            elif str_val == "b":
                mov.back()

            sensor_data = {
                "distance": ult.get_distance(),
                "speed": 0.1,
                "battery": 5,
                "direction": "l" 
            }

            json_data = json.dumps(sensor_data)
            client.sendall(json_data.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def start_server():
    """Starts the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", PORT))
        server_socket.listen()

        print(f"🚀 Server listening on port {PORT}")

        try:
            while True:
                client, client_info = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client, client_info), daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("\n❌ Server shutting down.")
        except Exception as e:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()
