from bleak import BleakAdvertiser
import asyncio

async def advertise():
    advertiser = BleakAdvertiser()
    await advertiser.start()
    print("Advertising started...")
    await asyncio.sleep(60)  # Advertise for 60 seconds
    await advertiser.stop()
    print("Advertising stopped.")

asyncio.run(advertise())