import asyncio
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import aiofiles

app = FastAPI(
    title="Log Streamer",
    description="A simple log streamer",
    version="0.1.0",
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Apache Logs Stream</title>
    </head>
    <body>
        <h1>Apache Access Log</h1>
        <pre id="accessLog"></pre>
        <h1>Apache Error Log</h1>
        <pre id="errorLog"></pre>
        <script src="/static/app.js"></script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    file_path = "YOUR_APACHE_ACCESS_LOG_PATH"
    last_size = 0

    while True:
        await asyncio.sleep(1)  # Poll every second
        current_size = os.path.getsize(file_path)
        if current_size > last_size:
            async with aiofiles.open(file_path, mode="r") as f:
                await f.seek(last_size)
                while new_line := await f.readline():
                    # If new line is just a blank line, new line char or empty string, skip it
                    if new_line in ["\n", "\r\n", ""]:
                        continue
                    await websocket.send_text(new_line)
            last_size = current_size
