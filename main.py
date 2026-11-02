import os, time, threading
from flask import Flask
from python_aternos import Client

app = Flask(__name__)

# Pega do painel do Render/Koyeb - NUNCA coloca senha aqui
USERNAME = os.getenv("ATERNOS_USER")  # jcodogn
PASSWORD = os.getenv("ATERNOS_PASS")  # sua senha nova

if not USERNAME or not PASSWORD:
    print("ERRO: Coloca ATERNOS_USER e ATERNOS_PASS no painel do Render!")

client = Client.from_credentials(USERNAME, PASSWORD)
client.login()
print("Login Aternos OK!")

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
            print(f"IP: jcodogn.aternos.me:58029 | Status: {srv.status} | Java 26.3")
            if "offline" in str(srv.status).lower():
                print(">>> LIGANDO SERVIDOR <<<")
                srv.start()
                time.sleep(50)
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
    return f"""
    <h1>✅ BOT 24H ONLINE</h1>
    <p><b>IP:</b> jcodogn.aternos.me:58029</p>
    <p><b>Versão:</b> Java 26.3</p>
    <p><b>Status:</b> {srv.status}</p>
    <p><b>Players:</b> {srv.players_count}</p>
    <br>
    <h2><a href='/start'>▶️ LIGAR SERVIDOR AGORA</a></h2>
    """

@app.route("/start")
def start():
    srv = get_server()
    srv.start()
    return f"Ligando jcodogn.aternos.me:58029 - Entra no Mine em 2 min! Java 26.3"

@app.route("/status")
def status():
    srv = get_server()
    return {"ip": "jcodogn.aternos.me:58029", "version": "Java 26.3", "status": str(srv.status), "players": str(srv.players_count)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
