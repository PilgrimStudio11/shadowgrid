import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
OWNER_FILE = "architect.lock"
network_stats = {
    "nodes_online": 142, # Примерное число до реальных данных
    "total_power": "4.2 TFlops",
    "active_cities": "Москва, Новосибирск, Лондон..."
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Технологичный лендинг, который видят пользователи"""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>ShadowGrid | Secure DEPIN</title>
        <style>
            body {{ background: #050505; color: #00F0FF; font-family: 'Consolas', monospace; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }}
            .container {{ border: 1px solid #00F0FF; padding: 50px; text-align: center; box-shadow: 0 0 30px rgba(0, 240, 255, 0.2); width: 600px; }}
            h1 {{ font-size: 3em; letter-spacing: 5px; text-shadow: 0 0 15px #00F0FF; }}
            .desc {{ color: #888; margin-bottom: 30px; border-bottom: 1px solid #222; padding-bottom: 20px; }}
            .stats {{ margin-top: 20px; padding: 15px; background: #000; border: 1px solid #333; }}
            .stats p {{ margin: 5px 0; color: #FF003C; }}
            .btn {{ display: inline-block; padding: 15px 30px; border: 1px solid #FF003C; color: #FF003C; text-decoration: none; font-weight: bold; transition: 0.3s; margin-top: 30px; }}
            .btn:hover {{ background: #FF003C; color: #000; box-shadow: 0 0 20px #FF003C; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SHADOWGRID</h1>
            <p class="desc">Децентрализованная автономная инфраструктура (DePIN) для приватности и вычислений.</p>
            
            <div class="stats">
                <p>Узлов онлайн: {network_stats["nodes_online"]}</p>
                <p>Общая мощность: {network_stats["total_power"]}</p>
                <p>Активные города: {network_stats["active_cities"]}</p>
            </div>

            <a href="/download" class="btn">ПОЛУЧИТЬ ДОСТУП (v1.0)</a>
        </div>
    </body>
    </html>
    """

@app.websocket("/ws/master")
async def master_beacon(websocket: WebSocket):
    """Скрытый WebSocket-канал для вашей Админки"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("command") == "HANDSHAKE":
                master_id = data.get("master_id")
                if not os.path.exists(OWNER_FILE):
                    with open(OWNER_FILE, "w") as f: f.write(master_id)
                    await websocket.send_json({"status": "LINKED", "msg": "Хаб GidHab привязан."})
                else:
                    with open(OWNER_FILE, "r") as f: saved_id = f.read()
                    if saved_id == master_id:
                        await websocket.send_json({"status": "READY", "stats": network_stats})
                    else:
                        await websocket.send_json({"status": "DENIED"})
                        await websocket.close()
    except WebSocketDisconnect:
        pass

@app.get("/download")
async def download():
    return {"status": "pending", "message": "Билд мессенджера будет доступен после подписи Архитектором."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
