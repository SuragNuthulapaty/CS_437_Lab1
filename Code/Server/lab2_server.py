from bluezero import adapter, device, localGATT
import time

# Define a custom service UUID
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class MyService(localGATT.Service):
    def __init__(self, index):
        super().__init__(index, SERVICE_UUID, True)
        self.characteristic = MyCharacteristic(self)
        self.add_characteristic(self.characteristic)

class MyCharacteristic(localGATT.Characteristic):
    def __init__(self, service):
        super().__init__(0, CHAR_UUID,
                         ["read", "write"],
                         service)
        self.value = b"Hello from Raspberry Pi!"

    def ReadValue(self, options):
        print("Sending data to client")
        return self.value

    def WriteValue(self, value, options):
        print(f"Received from client: {bytes(value).decode()}")
        self.value = bytes(value)

# Start BLE server
app = localGATT.Application()
app.add_service(MyService(0))
app.start()
