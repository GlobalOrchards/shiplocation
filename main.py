import asyncio
import websockets
import json
import os

API_KEY = os.environ["API_KEY"]

async def listen_to_ais():
    uri = "wss://stream.aisstream.io/v0/stream"
    headers = {
        "Authorization": API_KEY
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        print("✅ Connected to AISStream")

        # This is the correct subscription message format per AISStream spec
        subscription = {
            "APIKey": API_KEY,
            "BoundingBoxes": [],
            "FilterMessageTypes": ["PositionReport"],
            "FilterMMSI": []
        }

        await websocket.send(json.dumps(subscription))
        print("📡 Subscribed! Waiting for messages...\n")

        try:
            async for message in websocket:
                data = json.loads(message)
                print(json.dumps(data, indent=2))
        except websockets.exceptions.ConnectionClosed as e:
            print("🚫 Connection closed:", e)

asyncio.run(listen_to_ais())