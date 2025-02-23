from gi.repository import GLib
from pydbus import SystemBus
import dbus
import time

BLUEZ_SERVICE_NAME = "org.bluez"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
ADAPTER_IFACE = "org.freedesktop.DBus.ObjectManager"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class Characteristic:
    def __init__(self):
        self.value = b"Hello from Raspberry Pi!"

    def ReadValue(self, options):
        print("Client read request")
        return dbus.Array(self.value, signature="y")

    def WriteValue(self, value, options):
        print(f"Received from client: {bytes(value).decode()}")
        self.value = bytes(value)

def setup_ble():
    bus = SystemBus()
    adapter = bus.get(BLUEZ_SERVICE_NAME, "/org/bluez/hci0")

    # Ensure BLE is enabled
    adapter.Powered = True
    adapter.Discoverable = True

    print("BLE Server Started. Waiting for connections...")
    mainloop = GLib.MainLoop()
    mainloop.run()

setup_ble()
