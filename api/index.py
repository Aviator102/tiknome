from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Função para consultar a existência do usuário no TikTok
def consultar_exist(username):
    url = f"https://countik.com/api/exist/{username}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://countik.com/tiktok-likes-generator"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para consultar os vídeos do usuário no TikTok
def consultar_analyze(sec_uid):
    all_videos = []
    page = 1
    while True:
        url = f"https://countik.com/api/analyze/?sec_user_id={sec_uid}&page={page}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://countik.com/tiktok-likes-generator"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if not data.get("videos"):
                break  # Se não houver mais vídeos, parar a busca
            all_videos.extend(data.get("videos", []))
            page += 1  # Ir para a próxima página
        else:
            break

    return all_videos

# Rota para renderizar a página inicial
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        if not username:
            return render_template("index.html", message="Por favor, insira um nome de usuário.")
        
        dados_exist = consultar_exist(username)
        if dados_exist:
            sec_uid = dados_exist.get("sec_uid")
            if sec_uid:
                dados_analyze = consultar_analyze(sec_uid)
                if dados_analyze:
                    return render_template("index.html", videos=dados_analyze)
                else:
                    return render_template("index.html", message="Nenhum vídeo encontrado.")
            else:
                return render_template("index.html", message="sec_uid não encontrado.")
        else:
            return render_template("index.html", message="Erro ao consultar o usuário.")

    return render_template("index.html")

# Iniciar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
