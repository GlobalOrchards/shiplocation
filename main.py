import asyncio
import websockets
import json
import os

API_KEY = os.environ["API_KEY"]  # Make sure to set this in Render's environment variables

async def listen_to_ais():
    url = f"wss://stream.aisstream.io/v0/stream"
    headers = {
        "Authorization": API_KEY
    }

    async with websockets.connect(url, extra_headers=headers) as websocket:
        print("Connected to AISStream...")
        async for message in websocket:
            data = json.loads(message)
            print(json.dumps(data, indent=2))  # Prettified output

asyncio.run(listen_to_ais())