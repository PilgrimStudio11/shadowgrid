import os
import json
from flask import Flask, send_from_directory
from flask_sock import Sock

# Настройка статической папки для 2026: корень проекта
app = Flask(__name__, static_folder='.', static_url_path='')
sock = Sock(app)

# Хранилище состояния в памяти (для Railway)
STATE = {
    "ARCHITECT_PUB_KEY": None,
    "LAST_SIGNAL": None
}

@app.route('/')
def serve_index():
    """Явная раздача index.html"""
    return send_from_directory('.', 'index.html')

@sock.route('/ws/master')
def master_socket(ws):
    global STATE
    print("Админка инициировала подключение")
    while True:
        try:
            data = ws.receive()
            if not data: continue
            msg = json.loads(data)
            
            # РУКОПОЖАТИЕ (HANDSHAKE)
            if msg.get('command') == "HANDSHAKE":
                m_id = msg.get('master_id')
                if STATE["ARCHITECT_PUB_KEY"] is None:
                    STATE["ARCHITECT_PUB_KEY"] = m_id
                    ws.send(json.dumps({"status": "LINKED", "msg": "Вы установлены как Архитектор"}))
                elif STATE["ARCHITECT_PUB_KEY"] == m_id:
                    ws.send(json.dumps({"status": "READY", "msg": "Связь подтверждена"}))
                else:
                    ws.send(json.dumps({"status": "DENIED", "msg": "Доступ запрещен: владелец уже есть"}))

            # ТРАНСЛЯЦИЯ СИГНАЛА
            elif msg.get('command') == "BROADCAST_SIGNAL":
                signal = msg.get('signal')
                if signal and signal.get('pub') == STATE["ARCHITECT_PUB_KEY"]:
                    STATE["LAST_SIGNAL"] = signal
                    print(f"Сигнал получен: {signal['msg']['magnet']}")
                    ws.send(json.dumps({"status": "SUCCESS", "msg": "Сигнал транслирован"}))
                else:
                    ws.send(json.dumps({"status": "ERROR", "msg": "Крипто-подпись не совпадает"}))

        except Exception as e:
            print(f"WS Error: {e}")
            break

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
