
import requests
from flask import Flask, render_template, request, jsonify
import webbrowser
import pyperclip  # Para copiar para a área de transferência

app = Flask(__name__)

# Função para enviar a requisição para o TikTok e exibir o resultado
def processar_urls(urls_tiktok):
    for url_tiktok in urls_tiktok:
        if url_tiktok.strip() == "":  # Se a URL estiver vazia, ignora
            continue
        try:
            # URL da API Tikdown
            api_url = "https://tikdown.com/proxy.php"
            payload = {'url': url_tiktok}
            headers = {
                'Referer': 'https://tikdown.com',
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            # Enviar a requisição POST
            response = requests.post(api_url, data=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()  # Parse a resposta JSON
                video_url = data['api']['mediaItems'][0]['mediaUrl']  # URL do vídeo
                file_url = obter_url_video(video_url)  # Faz outra requisição para obter o link de download do vídeo
                # Se o file_url for encontrado, inicia o download automaticamente
                if file_url:
                    webbrowser.open(file_url)  # Abre o link diretamente no navegador para download
            else:
                return f"Erro na requisição. Código de status: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar à API: {e}"

    return "Processamento concluído."

# Função para fazer a requisição à URL do vídeo e obter o link de download
def obter_url_video(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            data = response.json()  # Parse da resposta JSON
            file_url = data.get('fileUrl', None)  # Obtém o fileUrl da resposta
            return file_url
        else:
            return f"Erro ao acessar a URL do vídeo. Código de status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a URL do vídeo: {e}"

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if not username:
            return render_template('index.html', message="Por favor, insira um nome de usuário.")
        
        dados_exist = consultar_exist(username)
        if dados_exist:
            sec_uid = dados_exist.get("sec_uid")
            if sec_uid:
                dados_analyze = consultar_analyze(sec_uid)
                if dados_analyze:
                    return render_template('index.html', message=f"Vídeos encontrados: {len(dados_analyze)}", videos=dados_analyze)
                else:
                    return render_template('index.html', message="Nenhum vídeo encontrado.")
            else:
                return render_template('index.html', message="sec_uid não encontrado.")
        else:
            return render_template('index.html', message="Falha ao obter dados do usuário.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
