import os, time, threading
from flask import Flask, jsonify
from python_aternos import Client

app = Flask(__name__)

USERNAME = os.getenv("ATERNOS_USER") # jcodogn
PASSWORD = os.getenv("ATERNOS_PASS") # admin123
client = Client.from_credentials(USERNAME, PASSWORD)
client.login()

def get_server():
    servers = client.list_servers()
    for s in servers:
        if "jcodogn" in str(s.address).lower():
            return s
    return servers[0]

# LOOP DO BOT 24H
def bot_loop():
    while True:
        try:
            srv = get_server()
            print(f"BOT: {srv.status}")
            if "offline" in str(srv.status).lower():
                srv.start()
            time.sleep(60)
        except:
            try:
                client.login()
            except:
                pass
            time.sleep(30)

threading.Thread(target=bot_loop, daemon=True).start()

# SITE HTML
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>jcodogn - Minecraft Server 24H</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f0f0f;color:white;font-family:Arial;text-align:center;padding:20px}
.card{background:#1e1e1e;padding:25px;border-radius:15px;max-width:400px;margin:auto;box-shadow:0 0 20px #00ff8844}
.btn{background:#00c853;color:white;padding:18px 35px;border:none;border-radius:10px;font-size:22px;cursor:pointer;width:100%;font-weight:bold}
.btn:active{transform:scale(0.95)}
.status{font-size:18px;margin:15px 0}
.ip{background:#000;padding:12px;border-radius:8px;font-size:18px;margin:15px 0;letter-spacing:1px}
.online{color:#00ff88} .offline{color:#ff4444} .loading{color:#ffaa00}
</style>
</head>
<body>
<div class="card">
<h1>⛏️ jcodogn</h1>
<div class="ip">jcodogn.aternos.me:58029<br><small>Java 26.3</small></div>
<div class="status" id="status">Carregando...</div>
<div class="status" id="players"></div>
<button class="btn" onclick="ligar()">▶️ LIGAR SERVIDOR</button>
<p style="margin-top:20px;font-size:13px;color:#888">Bot 24h rodando - PC pode ficar desligado<br>Atualiza a cada 5 segundos</p>
</div>
<script>
async function update(){
  try{
    let r = await fetch('/api/status');
    let j = await r.json();
    let el = document.getElementById('status');
    el.textContent = 'Status: ' + j.status;
    el.className = 'status ' + (j.status.includes('online') ? 'online' : j.status.includes('offline') ? 'offline' : 'loading');
    document.getElementById('players').textContent = 'Players: ' + j.players + ' / Online: ' + j.status;
  }catch(e){}
}
async function ligar(){
  document.getElementById('status').textContent = 'LIGANDO... aguarde na fila do Aternos';
  await fetch('/start');
  setTimeout(update, 3000);
}
setInterval(update, 5000);
update();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/start")
def start():
    srv = get_server()
    srv.start()
    return jsonify({"ok": True, "msg": f"Ligando {srv.address}"})

@app.route("/api/status")
def api_status():
    try:
        srv = get_server()
        return jsonify({
            "ip": "jcodogn.aternos.me:58029",
            "address": str(srv.address),
            "status": str(srv.status),
            "players": str(srv.players_count),
            "version": "Java 26.3",
            "port": "58029"
        })
    except Exception as e:
        return jsonify({"status": "erro", "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
