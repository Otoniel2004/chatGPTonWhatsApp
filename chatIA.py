from key import API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
import requests
import time

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

headers = {"Authorization": f"Bearer {API_KEY}"}

link = "https://api.openai.com/v1/chat/completions" # Link padrão

# Listar todas as mensagens enviadas
messages = client.messages.list(from_="whatsapp:+55", limit=1) # Adicionar número do WhatsApp

while True:
    
    # Leitor das perguntas
    last_message = messages[0]
    newMSG = last_message.body

    oldMSG = newMSG

    while newMSG == oldMSG:
        messages = client.messages.list(from_="whatsapp:+55", limit=1) # Adicionar seu número de WhatsApp padrão
        last_message = messages[0]
        newMSG = last_message.body
        if (newMSG != oldMSG):
                break
        time.sleep(1)

    # Consumindo API chatGPT
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": newMSG}
        ],
        "max_tokens": 150
    }

    request = requests.post(link, headers=headers, json=data)

    # Convertendo a resposta para JSON
    response_data = request.json()  

    # Envio de Respostas ao WhatsApp
    message = client.messages.create(
        from_='whatsapp:+1', # Adicionar número de WhatsApp grátis da Twilio
        body= response_data['choices'][0]['message']['content'],
        to='whatsapp:+55' # Adicionar seu número de WhatsApp padrão
    )
