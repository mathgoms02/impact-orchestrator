import requests
import os

from dotenv import load_dotenv

load_dotenv()

# 1. COLE A CHAVE AQUI DIRETAMENTE ENTRE AS ASPAS (substitua o texto)
# Certifique-se de copiar o "Value/Secret" lá do site da IBM, e não o "ID"
MINHA_CHAVE_IAM = os.getenv('WATSONX_API_KEY')

print(f"Testando a chave que começa com: {MINHA_CHAVE_IAM[:5]}...")

# 2. Fazendo a requisição
url_token = 'https://iam.cloud.ibm.com/identity/token'
data_token = {
    "apikey": MINHA_CHAVE_IAM, 
    "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
}

response = requests.post(url_token, data=data_token)

# 3. Analisando o resultado
if response.status_code == 200:
    print("\n✅ SUCESSO! A chave funciona!")
    print("Token gerado:", response.json()["access_token"][:20], "...")
    print("Response: ", response.json())
else:
    print("\n❌ ERRO! A IBM recusou ESTA string exata.")
    print("Detalhes:", response.json())