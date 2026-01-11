import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Файл для фиксации вашей власти на сервере
OWNER_FILE = "architect.lock"
# Хранилище оперативных данных о сети (в памяти сервера)
network_stats = {
    "nodes_online": 0,
    "total_power": "0.0 TFlops",
    "active_cities": []
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Лендинг, который видят обычные пользователи"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ShadowGrid | Genesis Beacon</title>
        <style>
            body { background: #050505; color: #00F0FF; font-family: 'Consolas', monospace; margin: 0; display: flex; align-items: center; justify-content: center; height: 100vh; }
            .container { border: 1px solid #00F0FF; padding: 50px; text-align: center; box-shadow: 0 0 30px rgba(0, 240, 255, 0.2); position: relative; }
            .glitch { font-size: 3em; font-weight: bold; text-transform: uppercase; letter-spacing: 10px; margin-bottom: 20px; }
            .status-bar { font-size: 0.8em; color: #555; margin-top: 30px; border-top: 1px solid #222; padding-top: 10px; }
            .btn { display: inline-block; padding: 15px 30px; border: 1px solid #FF003C; color: #FF003C; text-decoration: none; font-weight: bold; transition: 0.3s; margin-top: 20px; }
            .btn:hover { background: #FF003C; color: #000; box-shadow: 0 0 20px #FF003C; }
            .scanline { width: 100%; height: 2px; background: rgba(0, 240, 255, 0.1); position: absolute; top: 0; left: 0; animation: scan 4s linear infinite; }
            @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="scanline"></div>
            <div class="glitch">ShadowGrid</div>
            <p>ПРОТОКОЛ ДЕЦЕНТРАЛИЗОВАННОЙ АНОНИМНОСТИ АКТИВИРОВАН</p>
            <a href="/download" class="btn">ПОЛУЧИТЬ ДОСТУП (v1.0)</a>
            <div class="status-bar">BEACON_STATUS: ONLINE // ENCRYPTION: Ed25519 // MESH: READY</div>
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
            # Ожидание команды от Админки
            data = await websocket.receive_json()
            command = data.get("command")
            master_id = data.get("master_id")

            # Протокол HANDSHAKE (Рукопожатие)
            if command == "HANDSHAKE":
                if not os.path.exists(OWNER_FILE):
                    # Если Хаб "чистый", записываем ваш ID как владельца
                    with open(OWNER_FILE, "w") as f:
                        f.write(master_id)
                    await websocket.send_json({"status": "LINKED", "msg": "Хаб GidHab привязан к вашему Master ID."})
                else:
                    # Проверка владельца
                    with open(OWNER_FILE, "r") as f:
                        saved_id = f.read()
                    if saved_id == master_id:
                        await websocket.send_json({
                            "status": "READY", 
                            "stats": network_stats,
                            "msg": "Доступ Архитектора подтвержден."
                        })
                    else:
                        await websocket.send_json({"status": "DENIED", "msg": "Ошибка: Ключ не совпадает."})
                        await websocket.close(code=1008)

            # Команда на получение данных для карты
            elif command == "GET_TELEMETRY":
                await websocket.send_json({"status": "DATA", "payload": network_stats})

    except WebSocketDisconnect:
        pass

@app.get("/download")
async def download():
    return {"status": "pending", "message": "Билд мессенджера будет доступен после подписи Архитектором."}

if __name__ == "__main__":
    # GidHab передает порт в переменной окружения PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
