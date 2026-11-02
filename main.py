import os, time, threading
from flask import Flask
from python_aternos import Client

app = Flask(__name__)
USERNAME = os.getenv("ATERNOS_USER")
PASSWORD = os.getenv("ATERNOS_PASS")

print("Iniciando...")
client = Client.from_credentials(USERNAME, PASSWORD)
client.login()

def get_server():
    servers = client.list_servers()
    for s in servers:
        if "jcodogn" in str(s.address).lower():
            return s
    return servers[0]

def bot_loop():
    while True:
        try:
            srv = get_server()
            print(f"Servidor: {srv.address} | Status: {srv.status} | Players: {srv.players_count}")
            if "offline" in str(srv.status).lower():
                print("LIGANDO jcodogn.aternos.me:58029")
                srv.start()
            time.sleep(60)
        except Exception as e:
            print(f"Erro: {e}")
            try:
                client.login()
            except:
                pass
            time.sleep(30)

threading.Thread(target=bot_loop, daemon=True).start()

@app.route("/")
def home():
    srv = get_server()
    return f"<h1>BOT 24H jcodogn.aternos.me:58029</h1><p>{srv.address} - {srv.status}</p><a href='/start'>LIGAR</a> | <a href='/status'>STATUS</a>"

@app.route("/start")
def start():
    srv = get_server()
    srv.start()
    return f"Ligando {srv.address}:58029..."

@app.route("/status")
def status():
    srv = get_server()
    return {"ip": "jcodogn.aternos.me:58029", "address": str(srv.address), "status": str(srv.status)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
