import socket
import threading

HOST = "10.195.7.214"  # IP address of your Raspberry Pi
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

def handle_client(client, client_info):
    """Handles communication with a connected client."""
    print(f"🟢 Connected to {client_info}")
    try:
        while True:
            data = client.recv(1024)  # Receive data (up to 1024 bytes)
            if not data:
                print(f"🔴 Client {client_info} disconnected.")
                break  # Exit the loop if no data is received
            
            print(f"📩 Received from {client_info}: {data.decode()}")
            client.sendall(data)  # Echo back the received message
    except Exception as e:
        print(f"❌ Error with {client_info}: {e}")
    finally:
        client.close()
        print(f"🔌 Connection closed: {client_info}")

def start_server():
    """Starts the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse port if restarting
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"🚀 Server listening on {HOST}:{PORT}")

        try:
            while True:
                client, client_info = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client, client_info), daemon=True)
                client_thread.start()  # Start a new thread for each client
        except KeyboardInterrupt:
            print("\n🛑 Server shutting down.")
        except Exception as e:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()
