import os, time, threading, datetime
from flask import Flask, jsonify
from python_aternos import Client

app = Flask(__name__)
USERNAME = os.getenv("ATERNOS_USER")
PASSWORD = os.getenv("ATERNOS_PASS")
LOGS = []

def log(msg):
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    LOGS.append(f"[{hora}] {msg}")
    if len(LOGS) > 60: LOGS.pop(0)
    print(msg)

# NOVA FORMA DA BIBLIOTECA 3.0.6
client = Client()
client.login(USERNAME, PASSWORD)
log(f"Login OK - {USERNAME}")

def get_server():
    servers = client.list_servers()
    for s in servers:
        if "jcodogn" in str(s.domain).lower() or "jcodogn" in str(s.address).lower():
            return s
    return servers[0]

def bot_loop():
    while True:
        try:
            srv = get_server()
            log(f"Check: {srv.status} | Players: {srv.players_count}")
            if "offline" in str(srv.status).lower():
                log(">>> LIGANDO AUTOMATICO <<<")
                srv.start()
            time.sleep(55)
        except Exception as e:
            log(f"Erro: {e}")
            try: client.login(USERNAME, PASSWORD)
            except: pass
            time.sleep(20)

threading.Thread(target=bot_loop, daemon=True).start()

PANEL = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel jcodogn</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#0a0a0a;color:#fff}
.top{background:#111;padding:15px 20px;display:flex;justify-content:space-between;border-bottom:1px solid #222}
.top h2{color:#00ff88}
.container{max-width:900px;margin:20px auto;padding:0 15px;display:grid;grid-template-columns:1fr 1fr;gap:15px}
.card{background:#151515;border:1px solid #222;border-radius:14px;padding:20px}
.full{grid-column:1/-1}
.ipbox{background:#000;padding:12px;border-radius:8px;text-align:center;border:1px solid #00ff8840}
.btn{padding:14px;border-radius:10px;border:none;font-weight:bold;cursor:pointer;width:100%;font-size:16px;margin-top:8px}
.btn-green{background:#00c853;color:#fff} .btn-red{background:#222;color:#ff5555;border:1px solid #333} .btn-blue{background:#1e88e5;color:#fff}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:6px}
.online{background:#00ff88;box-shadow:0 0 8px #00ff88} .offline{background:#ff4444} .starting{background:#ffaa00}
.log{background:#000;height:220px;overflow:auto;padding:10px;font-family:monospace;font-size:12px;border-radius:8px;color:#aaa}
@media(max-width:700px){.container{grid-template-columns:1fr}}
</style></head><body>
<div class="top"><h2>⛏️ JCODO PANEL</h2><small style="color:#666">jcodogn.aternos.me:58029</small></div>
<div class="container">
<div class="card"><h3>Servidor</h3>
<div class="ipbox">jcodogn.aternos.me:58029<br><small style="color:#888">Java 26.3</small></div>
<div style="margin:15px 0"><span id="dot" class="dot offline"></span><span id="st">Carregando...</span></div>
<div id="players" style="color:#888">Players: -</div>
<button class="btn btn-green" onclick="cmd('start')">▶️ LIGAR</button>
<button class="btn btn-red" onclick="cmd('stop')">⏹️ DESLIGAR</button>
<button class="btn btn-blue" onclick="cmd('restart')">🔄 REINICIAR</button>
</div>
<div class="card"><h3>Info</h3>
<p>📦 Java 26.3</p><p>🌐 jcodogn.aternos.me</p><p>🔌 58029</p><p>🤖 Bot 24h Ativo</p>
<div style="margin-top:15px;background:#00ff8811;padding:10px;border-radius:8px;border:1px solid #00ff8822"><small>Qualquer pessoa com esse link pode ligar o servidor mesmo com seu PC desligado.</small></div>
</div>
<div class="card full"><h3>📋 Logs</h3><div class="log" id="logs"></div></div>
</div>
<script>
async function refresh(){
 let r=await fetch('/api/status'); let j=await r.json();
 document.getElementById('st').innerText=j.status.toUpperCase();
 document.getElementById('players').innerText='Players: '+j.players;
 let dot=document.getElementById('dot');
 dot.className='dot '+(j.status.includes('online')?'online':j.status.includes('offline')?'offline':'starting');
 let l=await (await fetch('/api/logs')).json();
 document.getElementById('logs').innerHTML=l.logs.map(x=>'<div>'+x+'</div>').join('');
}
async function cmd(a){ document.getElementById('st').innerText='ENVIANDO...'; await fetch('/api/'+a); setTimeout(refresh,2000); }
setInterval(refresh,4000); refresh();
</script></body></html>
"""

@app.route("/")
def home(): return PANEL
@app.route("/api/start")
def api_start():
    try: get_server().start(); log("MANUAL: LIGAR"); return jsonify(ok=True)
    except Exception as e: return jsonify(ok=False, error=str(e))
@app.route("/api/stop")
def api_stop():
    try: get_server().stop(); log("MANUAL: DESLIGAR"); return jsonify(ok=True)
    except Exception as e: return jsonify(ok=False, error=str(e))
@app.route("/api/restart")
def api_restart():
    try: s=get_server(); s.restart(); log("MANUAL: REINICIAR"); return jsonify(ok=True)
    except Exception as e: return jsonify(ok=False, error=str(e))
@app.route("/api/status")
def api_status():
    try:
        s=get_server()
        return jsonify(status=str(s.status), players=str(s.players_count))
    except Exception as e: return jsonify(status=str(e), players="-")
@app.route("/api/logs")
def api_logs(): return jsonify(logs=list(reversed(LOGS))[-50:])
@app.route("/start")
def start(): get_server().start(); return "Ligando..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
