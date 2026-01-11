import os
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
OWNER_FILE = "architect.lock"
network_stats = {
    "nodes_online": 0,
    "total_power": "0.0 TFlops",
    "active_cities": "Ожидание данных..."
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Технологичный светлый лендинг"""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>ShadowGrid | Безопасная Сеть</title>
        <style>
            body {{ background: #FFFFFF; color: #000000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }}
            .container {{ border: 1px solid #AAA; padding: 40px; text-align: center; width: 600px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.5em; color: #0066cc; }}
            p {{ color: #555; }}
            .stats {{ margin-top: 20px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; }}
            #node-count {{ font-weight: bold; color: #FF003C; font-size: 1.2em; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #0066cc; color: #FFF; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ShadowGrid Network</h1>
            <p>Децентрализованная инфраструктура, которой вы можете доверять.</p>
            
            <div class="stats">
                <p>Узлов онлайн: <span id="node-count">Загрузка...</span></p>
            </div>
            
            <a href="/download" class="btn">Скачать приложение</a>
        </div>

        <script>
            // WebSocket для обновления данных в реальном времени
            const ws = new WebSocket('wss://' + window.location.host + '/ws/master');
            ws.onmessage = function(event) {{
                const data = JSON.parse(event.data);
                if (data.status === 'DATA') {{
                    document.getElementById('node-count').innerText = data.payload.nodes_online;
                }}
            }};
            // В будущем здесь будет код для отправки запроса на данные
        </script>
    </body>
    </html>
    """

@app.websocket("/ws/master")
async def master_beacon(websocket: WebSocket):
    """Скрытый WebSocket-канал для вашей Админки и Лендинга"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("command") == "HANDSHAKE":
                master_id = data.get("master_id")
                if not os.path.exists(OWNER_FILE):
                    with open(OWNER_FILE, "w") as f: f.write(master_id)
                    await websocket.send_json({"status": "LINKED"})
                else:
                    with open(OWNER_FILE, "r") as f: saved_id = f.read()
                    if saved_id == master_id:
                        await websocket.send_json({"status": "READY", "stats": network_stats})
            # Отправка данных на лендинг (заглушка)
            await websocket.send_json({"status": "DATA", "payload": {"nodes_online": 150}})

    except WebSocketDisconnect:
        pass

@app.get("/download")
async def download():
    return {"msg": "Ссылка на билд появится после загрузки через Админку."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
