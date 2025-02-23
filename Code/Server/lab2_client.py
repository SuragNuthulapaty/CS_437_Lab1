from bleak import BleakScanner, BleakClient
import asyncio

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def connect_and_read():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found {device.name} - {device.address}")
        if SERVICE_UUID in device.metadata.get("uuids", []):
            async with BleakClient(device.address) as client:
                value = await client.read_gatt_char(CHAR_UUID)
                print(f"Received: {value.decode()}")

asyncio.run(connect_and_read())
