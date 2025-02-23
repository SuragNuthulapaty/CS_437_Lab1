import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def connect_and_interact():
    devices = await BleakScanner.discover()
    raspberry_pi = None

    for device in devices:
        if SERVICE_UUID in device.metadata.get("uuids", []):
            raspberry_pi = device
            break

    if not raspberry_pi:
        print("Could not find Raspberry Pi server.")
        return

    async with BleakClient(raspberry_pi.address) as client:
        # Read data
        value = await client.read_gatt_char(CHAR_UUID)
        print(f"Received: {value.decode()}")

        # Write data
        await client.write_gatt_char(CHAR_UUID, b"Hello from MacBook!")
        print("Sent message to Raspberry Pi.")

asyncio.run(connect_and_interact())
