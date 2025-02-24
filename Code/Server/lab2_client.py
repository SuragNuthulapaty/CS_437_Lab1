import serial

mac_serial_port = "/dev/cu.Bluetooth-Incoming-Port"  # Update this if necessary
client = serial.Serial(mac_serial_port, baudrate=9600, timeout=1)

client.write("Hello, Pi!\n".encode())

response = client.readline().decode().strip()
print(f"Response: {response}")

client.close()
