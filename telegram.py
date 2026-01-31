import requests
from config import BOT_TOKEN, CHAT_ID, PORTA


def obter_ip_externo():
    try:
        resposta = requests.get("https://api.ipify.org?format=json", timeout=5)
        resposta.raise_for_status()
        return resposta.json()["ip"]
    except Exception as e:
        return f"Erro ao obter IP: {e}"


def enviar_telegram(mensagem, url_acesso):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🔗 Acessar",
                        "url": url_acesso
                    }
                ]
            ]
        }
    }

    requests.post(url, json=payload, timeout=10)


def enviarMensagem():
    ip = obter_ip_externo()

    if "Erro" in str(ip):
        print(ip)
        return

    url_acesso = f"http://{ip}:{PORTA}"

    mensagem = (
        "🌐 *Servidor Online*\n\n"
        f"IP Externo: `{ip}`\n"
        f"Porta: `{PORTA}`"
    )

    enviar_telegram(mensagem, url_acesso)
    print("IP enviado para o Telegram com sucesso!")
