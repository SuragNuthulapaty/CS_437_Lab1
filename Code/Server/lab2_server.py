# from gi.repository import GLib
# from pydbus import SystemBus
# import dbus
# import time

# BLUEZ_SERVICE_NAME = "org.bluez"
# GATT_MANAGER_IFACE = "org.bluez.GattManager1"
# ADAPTER_IFACE = "org.freedesktop.DBus.ObjectManager"

# SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
# CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

# class Characteristic:
#     def __init__(self):
#         self.value = b"Hello from Raspberry Pi!"

#     def ReadValue(self, options):
#         print("Client read request")
#         return dbus.Array(self.value, signature="y")

#     def WriteValue(self, value, options):
#         print(f"Received from client: {bytes(value).decode()}")
#         self.value = bytes(value)

# def setup_ble():
#     bus = SystemBus()
#     adapter = bus.get(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")

#     # Ensure BLE is enabled
#     adapter.Powered = True
#     adapter.Discoverable = True

#     print("BLE Server Started. Waiting for connections...")
#     mainloop = GLib.MainLoop()
#     mainloop.run()

# setup_ble()

import constants
import bluetooth

hostMACAddress = constants.HOST # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        print("server recv from: ", clientInfo)
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
except: 
    print("Closing socket")
    client.close()
    s.close()