import os
import json
from flask import Flask, send_from_directory, jsonify
from flask_sock import Sock

app = Flask(__name__, static_folder='.', static_url_path='')
sock = Sock(app)

# Состояние системы: теперь ключ сохраняется после первого Handshake
STATE = {
    "ARCHITECT_PUB_KEY": None
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# НОВЫЙ ЭНДПОИНТ: Маяк отдает свой привязанный ключ фронтенду
@app.route('/api/get_key')
def get_key():
    return jsonify({"pub_key": STATE["ARCHITECT_PUB_KEY"]})

@sock.route('/ws/master')
def master_socket(ws):
    global STATE
    while True:
        try:
            data = ws.receive()
            if not data: continue
            msg = json.loads(data)
            
            if msg.get('command') == "HANDSHAKE":
                m_id = msg.get('master_id')
                # АВТОМАТИЧЕСКАЯ ПРИВЯЗКА ПРИ ПЕРВОМ ЗАПУСКЕ
                if STATE["ARCHITECT_PUB_KEY"] is None:
                    STATE["ARCHITECT_PUB_KEY"] = m_id
                    print(f"МАЯК ПРИВЯЗАН К ARCHITECT_ID: {m_id}")
                    ws.send(json.dumps({"status": "LINKED", "msg": "Вы установлены как владелец."}))
                elif STATE["ARCHITECT_PUB_KEY"] == m_id:
                    ws.send(json.dumps({"status": "READY", "msg": "Связь подтверждена."}))
                else:
                    ws.send(json.dumps({"status": "DENIED", "msg": "Доступ запрещен."}))
            
            elif msg.get('command') == "BROADCAST_SIGNAL":
                # Здесь логика отправки в GunDB
                ws.send(json.dumps({"status": "SUCCESS", "msg": "Сигнал ушел в Grid"}))

        except Exception as e:
            break

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
