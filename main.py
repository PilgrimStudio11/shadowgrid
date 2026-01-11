import os
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
OWNER_FILE = "architect.lock"
# Хранилище реальных анонимных данных (в памяти сервера)
active_nodes = {
    "count": 0,
    "locations": [] # [{"lat": 55.75, "lon": 37.61, "count": 120}]
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Лендинг с интерактивной картой Leaflet.js"""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ShadowGrid | Безопасная Сеть</title>
        <link rel="stylesheet" href="unpkg.com" />
        <script src="unpkg.com"></script>
        <style>
            body {{ background: #FFFFFF; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }}
            .container {{ padding: 20px; text-align: center; width: 90%; max-width: 800px; }}
            h1 {{ color: #0066cc; }}
            #map {{ height: 500px; width: 100%; margin-top: 20px; }}
            .stats {{ margin-bottom: 10px; font-weight: bold; }}
            .btn {{ padding: 10px 20px; background: #0066cc; color: #FFF; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ShadowGrid Network Status</h1>
            <p class="stats">Узлов онлайн: <span id="node-count">0</span></p>
            <div id="map"></div>
            <a href="/download" class="btn">Скачать приложение</a>
        </div>

        <script>
            const map = L.map('map').setView([20, 0], 2);
            // Используем черно-белую карту для стиля контурной карты
            L.tileLayer('https://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {{
                maxZoom: 18,
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);

            const ws = new WebSocket('wss://' + window.location.host + '/ws/data');

            ws.onmessage = function(event) {{
                const data = JSON.parse(event.data);
                if (data.status === 'UPDATE') {{
                    document.getElementById('node-count').innerText = data.payload.count;
                    // Очистка старых маркеров и добавление новых
                    map.eachLayer(function (layer) {{
                        if (!!layer._leaflet_id && layer._leaflet_id !== map._leaflet_id) {{
                            map.removeLayer(layer);
                        }}
                    }});
                    data.payload.locations.forEach(loc => {{
                        L.circleMarker([loc.lat, loc.lon], {{color: 'red', fillColor: '#f03', fillOpacity: 0.8, radius: Math.log(loc.count) * 4}}).addTo(map)
                         .bindPopup(`Узлов: ${loc.count}`);
                    }});
                }}
            }};
        </script>
    </body>
    </html>
    """

# Канал для получения реальных данных от клиентов (будущего мессенджера)
@app.websocket("/ws/data")
async def data_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        # Имитация получения данных от 150 клиентов
        active_nodes["count"] = 150
        active_nodes["locations"] = [{"lat": 55.75, "lon": 37.61, "count": 120}, {"lat": 51.5, "lon": -0.1, "count": 30}]
        
        while True:
            # Отправка обновлений на лендинг каждые 10 секунд
            await websocket.send_json({"status": "UPDATE", "payload": active_nodes})
            await websocket.receive_text() # Ожидание пинга от клиента
            time.sleep(10)
    except WebSocketDisconnect:
        pass

# ... (остальной код FastAPI для /ws/master и /download без изменений) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

