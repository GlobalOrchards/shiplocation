import asyncio
from aisstream import Client

API_KEY = "YOUR_API_KEY_HERE"  # Replace this in a later step

async def run():
    async with Client(API_KEY) as client:
        async for message in client:
            print(message)

asyncio.run(run())