import os
from flask import Flask, render_template_string
import cloudscraper
from python_aternos import Client

app = Flask(__name__)

SESSION = os.getenv("ATERNOS_SESSION")
CF = os.getenv("CF_CLEARANCE")

def get_scraper():
    s = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
        delay=10
    )
    if CF:
        s.cookies.set('cf_clearance', CF, domain='.aternos.org')
        s.cookies.set('cf_clearance', CF, domain='aternos.org')
    if SESSION:
        s.cookies.set('ATERNOS_SESSION', SESSION, domain='.aternos.org')
    return s

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#0f0f0f;color:#fff;font-family:Arial;text-align:center;padding-top:50px}
.card{background:#1a1a1a;padding:30px;border-radius:20px;max-width:400px;margin:auto}
.btn{background:#2cc76a;color:#fff;border:none;padding:18px 40px;font-size:22px;border-radius:12px;cursor:pointer;width:100%}
</style></head><body><div class="card">
<h2>🎮 jcodogn.aternos.me:58029</h2>
<div>Status: <b>{{status}}</b></div><br>
<form method="POST" action="/start"><button class="btn">LIGAR SERVIDOR 🚀</button></form>
<p style="color:#888;font-size:11px;margin-top:15px">{{msg}}</p>
</div><script>setTimeout(()=>location.reload(),10000)</script></body></html>
"""

def get_server():
    scraper = get_scraper()
    # tenta os 2 jeitos de logar (versao antiga e nova da lib)
    try:
        client = Client.from_hashed_session(SESSION)
    except:
        client = Client()
        client.login_with_session(SESSION)
    
    # injeta o bypass do Cloudflare
    try:
        client.atserver.session = scraper
        client.atconnect.session = scraper
    except:
        pass
    try:
        client.session = scraper
    except:
        pass

    return client.list_servers()[0]

@app.route("/")
def home():
    if not SESSION:
        return "Configure ATSESSION no Render"
    try:
        serv = get_server()
        return render_template_string(HTML, status=serv.status, msg="Auto-refresh 10s")
    except Exception as e:
        return render_template_string(HTML, status="Erro", msg=str(e)[:300])

@app.route("/start", methods=["POST"])
def start():
    try:
        serv = get_server()
        serv.start()
        return "LIGANDO... entra no Mine em 1 min<br><a href='/'>Voltar</a>"
    except Exception as e:
        return f"Erro: {e}<br><a href='/'>Voltar</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
