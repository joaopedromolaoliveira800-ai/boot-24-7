import os, time, threading
from flask import Flask
from python_aternos import Client

app = Flask(__name__)
USERNAME = os.getenv("ATERNOS_USER")
PASSWORD = os.getenv("ATERNOS_PASS")
SERVER_NAME = "jcodogn.aternos.me" # SEU SERVIDOR

client = Client()

def login_aternos():
    while True:
        try:
            client.login(USERNAME, PASSWORD)
            print("Login Aternos OK!")
            return True
        except Exception as e:
            print(f"Erro login: {e}")
            time.sleep(30)

login_aternos()

def get_server():
    try:
        servers = client.account.list_servers()
        for s in servers:
            if "jcodogn" in str(s.address).lower():
                return s
        return servers[0]
    except Exception as e:
        print(f"Erro: {e}")
        login_aternos()
        return None

def bot_loop():
    while True:
        try:
            srv = get_server()
            if not srv:
                time.sleep(60)
                continue
            srv.fetch()
            status = str(srv.status).lower()
            print(f"[{srv.address}:{58029}] Status: {status}")
            if "offline" in status:
                print(">>> LIGANDO jcodogn.aternos.me:58029 <<<")
                srv.start()
                time.sleep(45)
            time.sleep(60)
        except Exception as e:
            print(f"Erro loop: {e}")
            time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()

@app.route("/")
def home():
    try:
        srv = get_server()
        srv.fetch()
        return f"""
        <h1>✅ BOT 24H - jcodogn.aternos.me:58029</h1>
        <p>IP: jcodogn.aternos.me:58029</p>
        <p>Status: {srv.status}</p>
        <p>Players: {srv.players_count}</p>
        <br>
        <h2><a href='/start'>▶️ CLIQUE AQUI PARA LIGAR O SERVIDOR</a></h2>
        <br>
        <a href='/status'>Ver JSON</a>
        """
    except Exception as e:
        return f"Bot iniciando... {e}"

@app.route("/start")
def start():
    srv = get_server()
    srv.start()
    return f"Ligando jcodogn.aternos.me:58029... Entre no Minecraft em 2 minutos! IP: jcodogn.aternos.me:58029"

@app.route("/status")
def status():
    srv = get_server()
    srv.fetch()
    return {"ip": "jcodogn.aternos.me:58029", "address": str(srv.address), "status": str(srv.status), "players": str(srv.players_count)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))