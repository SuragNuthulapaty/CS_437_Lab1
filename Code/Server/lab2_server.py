import serial

server = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)
print("Waiting for connection...")

while True:
    data = server.readline().decode().strip()
    if data:
        print(f"Received: {data}")
        server.write(f"Echo: {data}\n".encode())
