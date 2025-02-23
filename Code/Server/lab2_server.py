from bleak import BleakServer
import asyncio

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class SimpleBLEServer:
    def __init__(self):
        self.server = BleakServer()
        self.server.add_service(SERVICE_UUID, [CHAR_UUID])

    async def start(self):
        print("Starting BLE server...")
        await self.server.start()
        print(f"Server running with service UUID: {SERVICE_UUID}")

        while True:
            await asyncio.sleep(10)  # Keep running

async def main():
    server = SimpleBLEServer()
    await server.start()

asyncio.run(main())
