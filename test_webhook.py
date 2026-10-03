import requests

user_message = "Can you tell me about n8n in 3-4 lines"

request_message = {"message": user_message}
url = "WEBHOOK_URL"

resposne = requests.post(url, json=request_message)

print(resposne.status_code)
print(resposne.json()[0]["output"])