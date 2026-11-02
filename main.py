import os
from flask import Flask, render_template_string
from python_aternos import Client

app = Flask(__name__)

SESSION = os.getenv("ATERNOS_SESSION")

HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f0f0f;color:#fff;font-family:Arial;text-align:center;padding-top:50px}
.card{background:#1a1a1a;padding:30px;border-radius:20px;max-width:400px;margin:auto}
.btn{background:#2cc76a;color:#fff;border:none;padding:18px 40px;font-size:22px;border-radius:12px;cursor:pointer;width:100%}
.btn:disabled{background:gray}
.status{font-size:18px;margin:20px 0}
</style>
</head>
<body>
<div class="card">
<h2>🎮 jcodogn.aternos.me:58029</h2>
<div class="status">Status: <b>{{status}}</b></div>
<form method="POST" action="/start">
<button class="btn">{{'ONLINE ✅' if status=='Online' else 'LIGAR SERVIDOR 🚀'}}</button>
</form>
</div>
<script>setTimeout(()=>location.reload(),10000)</script>
</body>
</html>
"""

def get_aternos_client():
    atclient = Client()
    atclient.login_with_session(SESSION)  # <- AQUI TAVA O ERRO, agora corrigido
    return atclient

@app.route("/")
def home():
    try:
        atclient = get_aternos_client()
        serv = atclient.list_servers()[0]
        return render_template_string(HTML, status=serv.status)
    except Exception as e:
        return f"Erro: {e}"

@app.route("/start", methods=["POST"])
def start():
    try:
        atclient = get_aternos_client()
        serv = atclient.list_servers()[0]
        serv.start()
        return "Ligando... <a href='/'>Voltar</a>"
    except Exception as e:
        return f"Erro ao ligar: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
