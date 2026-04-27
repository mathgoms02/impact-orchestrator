import os
import requests
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Perfil, Voluntario, Crise
from .serializers import VoluntarioSerializer, CriseSerializer
from dotenv import load_dotenv

load_dotenv()

# --- AUTENTICAÇÃO E LOGIN ---
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['tipo'] = user.perfil.tipo if hasattr(user, 'perfil') else 'VOLUNTARIO'
        return token

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class RegistroUsuarioView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        tipo = request.data.get('tipo')

        if User.objects.filter(username=username).exists():
            return Response({"erro": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        Perfil.objects.create(user=user, tipo=tipo)
        return Response({"status": "Usuário criado!"}, status=status.HTTP_201_CREATED)

# --- INTEGRAÇÃO WATSONX (NATIVA) ---
def chamar_agente_watsonx(deployment_id, prompt_text):
    try:
        api_key = os.getenv('WATSONX_API_KEY')
        url_token = 'https://iam.cloud.ibm.com/identity/token'
        
        # 1. Pegar Token (CORREÇÃO: Usando dicionário para garantir o encode correto da API Key)
        token_data = {
            "apikey": api_key, 
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
        
        # O requests converte o dict automaticamente para form-urlencoded
        token_res = requests.post(url_token, data=token_data)
        
        # Se der erro 400 novamente, isso vai imprimir o motivo exato no terminal
        token_res.raise_for_status() 
        mltoken = token_res.json()['access_token']

        # 2. Chamar Agente
        url_agente = f'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{deployment_id}/ai_service?version=2021-05-01'
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt_text
                }
            ]
        }
        
        # Adicionando explicitamente o Content-Type como a IBM pede
        headers_agente = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {mltoken}'
        }
        
        response = requests.post(url_agente, json=payload, headers=headers_agente)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
        
    except requests.exceptions.HTTPError as err:
        # Pega a mensagem de erro detalhada da IBM (ex: API key inválida)
        return f"Erro na API da IBM: {err.response.text}"
    except Exception as e:
        return f"Erro interno na conexão com a IA: {str(e)}"

# --- ROTAS DA APLICAÇÃO ---
class AnalisarMatchView(APIView):
    def post(self, request):
        res = chamar_agente_watsonx(os.getenv('ID_AGENTE_MATCH'), 
                                    f"Analise o match. Crise: {request.data['crise']} / Voluntário: {request.data['voluntario']}")
        return Response({"match": res})

class NotificarAgenteView(APIView):
    def post(self, request):
        res = chamar_agente_watsonx(os.getenv('ID_AGENTE_COMUNICACAO'), 
                                    f"Notifique {request.data['nome']} sobre a tarefa {request.data['tarefa']} via {request.data['contato']}")
        return Response({"mensagem": res})

class VoluntarioListCreate(generics.ListCreateAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

class CriseListCreate(generics.ListCreateAPIView):
    queryset = Crise.objects.all().filter(ativa=True)
    serializer_class = CriseSerializer

    def perform_create(self, serializer):
        descricao_bruta = self.request.data.get('descricao_bruta')
        # A IA processa a descrição antes de salvar
        analise = chamar_agente_watsonx(os.getenv('ID_AGENTE_CRISE'), descricao_bruta)
        serializer.save(analise_ia=analise)