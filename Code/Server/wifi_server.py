import socket
import threading
import sys
import move
import Ultrasonic


ult = Ultrasonic.Ultrasonic()
mov = move.Move()
PORT = 65432

def handle_client(client, client_info):
    """Handles communication with a connected client."""
    print(f"🟢 Connected to {client_info}")
    try:
        while True:
            data = client.recv(1024)
            if not data:
                print(f"🔴 Client {client_info} disconnected.")
                break
        
            str_val = str((data.decode())).strip()

            print(str_val, str_val == "l")
            
            if str_val == "l":
                mov.left()
            elif str_val == 'r':
                mov.right()
            elif str_val == "f":
                mov.forward()
            elif str_val == "b":
                mov.back()

            v = ult.get_distance()
            bv = bytes(v)

            print(type(v), v, bv)
        
            client.sendall(str(v).encode())
    except Exception as e:
        pass
    finally:
        client.close()

def start_server(host):
    """Starts the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, PORT))
        server_socket.listen()

        print(f"Server listening on {host}:{PORT}")

        try:
            while True:
                client, client_info = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client, client_info), daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Server shutting down.")
        except Exception as e:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <host>")

    host = sys.argv[1]
    start_server(host)
