import os
import json
from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__, static_folder='.')
sock = Sock(app)

# В 2026 году Маяк запоминает ID первого подключившегося Архитектора
STATE = {
    "ARCHITECT_PUB_KEY": None,
    "LAST_SIGNAL": None
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@sock.route('/ws/master')
def master_socket(ws):
    global STATE
    while True:
        try:
            raw_data = ws.receive()
            msg = json.loads(raw_data)
            
            # 1. ПРИВЯЗКА ЛИЧНОСТИ (HANDSHAKE)
            if msg['command'] == "HANDSHAKE":
                incoming_id = msg['master_id']
                if STATE["ARCHITECT_PUB_KEY"] is None:
                    STATE["ARCHITECT_PUB_KEY"] = incoming_id
                    ws.send(json.dumps({"status": "LINKED", "msg": "Вы установлены как Архитектор. Ключ зафиксирован."}))
                elif STATE["ARCHITECT_PUB_KEY"] == incoming_id:
                    ws.send(json.dumps({"status": "READY", "msg": "Связь подтверждена."}))
                else:
                    ws.send(json.dumps({"status": "DENIED", "msg": "У Маяка уже есть владелец."}))

            # 2. ТРАНСЛЯЦИЯ ПОДПИСАННОГО СИГНАЛА
            elif msg['command'] == "BROADCAST_SIGNAL":
                signal = msg['signal'] # Формат из админки: {pub, msg, sig}
                if signal['pub'] == STATE["ARCHITECT_PUB_KEY"]:
                    STATE["LAST_SIGNAL"] = signal
                    # В 2026 здесь сигнал уходит в GunDB реле
                    print(f"СИГНАЛ ВЕРИФИЦИРОВАН: {signal['msg']['magnet']}")
                    ws.send(json.dumps({"status": "SUCCESS", "msg": "Сигнал транслирован в Grid"}))
                else:
                    ws.send(json.dumps({"status": "ERROR", "msg": "Ошибка: Ключ не совпадает."}))
                    
        except Exception as e:
            print(f"WebSocket Error: {e}")
            break

if __name__ == '__main__':
    # Порт для Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
