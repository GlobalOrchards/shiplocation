const express = require("express");
const WebSocket = require("ws");
const cors = require("cors");

const AIS_API_KEY = process.env.AISSTREAM_API_KEY;
const app = express();
app.use(cors());
const port = process.env.PORT || 3000;

// Store MMSI position data in memory
const vesselPositions = {};

// Connect to AISStream WebSocket
const ws = new WebSocket(`wss://stream.aisstream.io/v0/stream` , {
  headers: {
    "Authorization": 1b7f6abece7f84c76fc0128b6ee121d7469d576b
  }
});

ws.on("open", () => {
  console.log("Connected to AISStream");
  // Optionally, you can filter by MMSI or area
  ws.send(JSON.stringify({
    Apikey: AIS_API_KEY,
    BoundingBoxes: [[[-180, -90], [180, 90]]] // Global
  }));
});

ws.on("message", (data) => {
  const msg = JSON.parse(data);
  if (msg.MessageType === "PositionReport") {
    const mmsi = msg.MMSI;
    vesselPositions[mmsi] = {
      lat: msg.Lat,
      lon: msg.Lon,
      timestamp: new Date().toISOString()
    };
  }
});

app.get("/mmsi/:id", (req, res) => {
  const id = req.params.id;
  if (vesselPositions[id]) {
    res.json(vesselPositions[id]);
  } else {
    res.status(404).json({ error: "MMSI not found yet" });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});