import os, asyncio, json
import websockets
from datetime import datetime, timezone

BBOX = json.loads(os.getenv("AIS_BBOX", "[[[-180,-90],[180,90]]]"))  # world
APIKEY = os.getenv("AISSTREAM_API_KEY")

async def run():
    url = "wss://stream.aisstream.io/v0/stream"
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"APIKey": APIKEY, "BoundingBoxes": BBOX}))
        async for raw in ws:
            msg = json.loads(raw)
            if msg["MessageType"] == "PositionReport":
                p = msg["Message"]["PositionReport"]
                print(f"[{datetime.now(timezone.utc)}] {p['UserID']} "
                      f"{p['Latitude']:.4f},{p['Longitude']:.4f}")

if __name__ == "__main__":
    asyncio.run(run())