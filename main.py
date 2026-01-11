import os
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
OWNER_FILE = "architect.lock"
network_stats = {
    "nodes_online": 150, # Примерное число до реальных данных
    "total_power": "4.2 TFlops",
    "active_cities": "Москва, Новосибирск, Лондон..."
}

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Технологичный лендинг, который видят пользователи и инвесторы"""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ShadowGrid | Анонимность & DePIN Экосистема</title>
        <style>
            body {{ background: #050505; color: #00FF41; font-family: 'Consolas', monospace; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
            .container {{ border: 1px solid #00FF41; padding: 40px; text-align: center; width: 700px; box-shadow: 0 0 30px rgba(0, 255, 65, 0.2); }}
            h1 {{ font-size: 2.5em; letter-spacing: 4px; text-shadow: 0 0 10px #00FF41; }}
            .desc, .investor-pitch {{ color: #EEE; margin-bottom: 20px; }}
            .stats {{ margin-top: 20px; padding: 15px; background: #000; border: 1px solid #333; }}
            #node-count {{ font-weight: bold; color: #FF003C; font-size: 1.2em; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #00FF41; color: #000; text-decoration: none; border: none; cursor: pointer; margin-top: 20px; font-weight: bold; }}
            .btn:hover {{ background: #FFF; }}
            .footer {{ margin-top: 40px; font-size: 0.7em; color: #555; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>:: SHADOWGRID NETWORK ::</h1>
            <p class="desc">
                <strong>ShadowGrid</strong> — это не просто мессенджер. Это децентрализованная автономная инфраструктура (DePIN), где абсолютная анонимность встречается с реальной вычислительной мощностью.
            </p>
            <p>
                Мы предлагаем <strong>бесплатную защищенную связь (P2P/Mesh)</strong> в обмен на простаивающие ресурсы вашего ПК. Когда вы не используете компьютер, он становится узлом глобального суперкомпьютера, принося вам пассивный доход.
            </p>

            <div class="stats">
                <p>Узлов онлайн: <span id="node-count">{network_stats["nodes_online"]}</span> | Общая мощность: {network_stats["total_power"]}</p>
            </div>

            <p class="investor-pitch">
                Для инвесторов: Мы создаем самоподдерживающуюся экономику на 50 лет вперед. Ограниченная эмиссия (100 млн MYC), PoUW и растущий рынок децентрализованных вычислений. Присоединяйтесь к архитекторам будущего.
            </p>

            <a href="/download" class="btn">СКАЧАТЬ ПРИЛОЖЕНИЕ ShadowGrid</a>
            <div class="footer">
                Ваш ключ к абсолютной приватности и монетизации ресурсов.
            </div>
        </div>
        <script>
            // JS для обновления счетчика в реальном времени (пока заглушка)
            document.getElementById('node-count').innerText = {network_stats["nodes_online"]};
        </script>
    </body>
    </html>
    """
# ... (остальной код FastAPI и WebSocket без изменений) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
