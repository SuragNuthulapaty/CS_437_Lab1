# import asyncio
# from bleak import BleakScanner, BleakClient

# SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
# CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

# async def connect_and_interact():
#     devices = await BleakScanner.discover()
#     raspberry_pi = None

#     for device in devices:
#         if SERVICE_UUID in device.metadata.get("uuids", []):
#             raspberry_pi = device
#             break

#     if not raspberry_pi:
#         print("Could not find Raspberry Pi server.")
#         return

#     async with BleakClient(raspberry_pi.address) as client:
#         # Read data
#         value = await client.read_gatt_char(CHAR_UUID)
#         print(f"Received: {value.decode()}")

#         # Write data
#         await client.write_gatt_char(CHAR_UUID, b"Hello from MacBook!")
#         print("Sent message to Raspberry Pi.")

# asyncio.run(connect_and_interact())

import constants
import bluetooth

host = constants.HOST # The address of Raspberry PI Bluetooth adapter on the server.
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
while 1:
    text = input("Enter your message: ") # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    sock.send(text)

    data = sock.recv(1024)
    print("from server: ", data)

sock.close()
