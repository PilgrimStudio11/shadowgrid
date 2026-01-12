import os
import json
from flask import Flask, send_from_directory, request
from flask_sock import Sock # Добавьте flask-sock в requirements.txt

app = Flask(__name__, static_folder='.')
sock = Sock(app)

# В 2026 году мы храним ключ архитектора в памяти или простом файле
ARCHITECT_PUB_KEY = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@sock.route('/ws/master')
def master_socket(ws):
    global ARCHITECT_PUB_KEY
    while True:
        data = ws.receive()
        msg = json.loads(data)
        
        if msg['command'] == "HANDSHAKE":
            if ARCHITECT_PUB_KEY is None:
                ARCHITECT_PUB_KEY = msg['master_id']
                ws.send(json.dumps({"status": "LINKED", "msg": "Вы установлены как Архитектор"}))
            elif ARCHITECT_PUB_KEY == msg['master_id']:
                ws.send(json.dumps({"status": "READY", "msg": "Связь подтверждена"}))
            else:
                ws.send(json.dumps({"status": "DENIED", "msg": "У Маяка уже есть владелец"}))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
