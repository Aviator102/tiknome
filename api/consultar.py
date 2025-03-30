import requests
from flask import Flask, jsonify

app = Flask(__name__)

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
                break
            all_videos.extend(data.get("videos", []))
            page += 1
        else:
            break

    return all_videos

# Função serverless para Vercel
def vercel_handler(request):
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Nome de usuário não informado."}), 400

    dados_exist = consultar_exist(username)
    
    if dados_exist:
        sec_uid = dados_exist.get("sec_uid")
        if sec_uid:
            dados_analyze = consultar_analyze(sec_uid)
            return jsonify(dados_analyze)
        else:
            return jsonify({"error": "sec_uid não encontrado."}), 400
    else:
        return jsonify({"error": "Falha ao obter dados do usuário."}), 400

# Vercel precisa retornar esta função
def handler(request):
    return vercel_handler(request)
