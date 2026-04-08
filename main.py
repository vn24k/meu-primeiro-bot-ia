import os
import telebot
import requests

# --- CONFIGURAÇÃO DE SEGURANÇA (O RENDER VAI PREENCHER ISSO) ---
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
API_KEY_GROQ = os.getenv("API_KEY_GROQ")

bot = telebot.TeleBot(TOKEN_TELEGRAM)

def falar_com_ia(pergunta):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY_GROQ}"}
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Você é um consultor de elite. Responda de forma prática."},
            {"role": "user", "content": pergunta}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=20)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Erro na conexão com a IA."

@bot.message_handler(func=lambda m: True)
def responder(message):
    bot.send_chat_action(message.chat.id, 'typing')
    resposta = falar_com_ia(message.text)
    bot.reply_to(message, resposta)

if __name__ == "__main__":
    print("🚀 Robô Iniciado na Nuvem!")
    bot.polling(non_stop=True)
