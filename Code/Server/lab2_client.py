import asyncio
from bleak import BleakScanner

async def scan_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Address: {device.address}, Name: {device.name}")

if __name__ == "__main__":
    asyncio.run(scan_devices())