import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
OWNER_FILE = "architect.lock"
network_stats = {
    "nodes_online": 150,
    "total_power": "4.2 TFlops",
    "active_cities": "Москва, Новосибирск, Лондон..."
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Современный светлый лендинг с заглушкой для карты"""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ShadowGrid | Безопасная Сеть</title>
        <style>
            body {{ background: #FFFFFF; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
            .container {{ padding: 40px; text-align: center; width: 700px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-radius: 8px; background: #FFF; }}
            h1 {{ font-size: 2.5em; color: #0066cc; border-bottom: 2px solid #EEE; padding-bottom: 10px; }}
            p {{ color: #555; margin-bottom: 20px; }}
            .stats {{ margin-top: 20px; padding: 15px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 5px; }}
            #node-count {{ font-weight: bold; color: #FF003C; font-size: 1.2em; }}
            .map-placeholder {{ margin-top: 20px; padding: 50px; background: #eee; border-radius: 5px; border: 1px dashed #999; color: #777; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #0066cc; color: #FFF; text-decoration: none; border: none; border-radius: 5px; margin-top: 20px; font-weight: bold; }}
            .btn:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ShadowGrid Network</h1>
            <p>Децентрализованная инфраструктура, которой вы можете доверять.</p>
            
            <div class="stats">
                <p>Узлов онлайн: <span id="node-count">{network_stats["nodes_online"]}</span> | Общая мощность: {network_stats["total_power"]}</p>
            </div>

            <div class="map-placeholder">
                [ Заглушка для интерактивной контурной карты мира из вашего изображения ]
            </div>

            <a href="/download" class="btn">Скачать приложение</a>
        </div>
        <script>
            // JavaScript для обновления счетчика
            document.getElementById('node-count').innerText = {network_stats["nodes_online"]};
        </script>
    </body>
    </html>
    """

# ... (остальной код FastAPI и WebSocket без изменений) ...
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
