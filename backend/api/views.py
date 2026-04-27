import os
import requests
import json
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

def chamar_agente_watsonx(deployment_id, prompt_text):
    """Função core que conecta o Django aos Deployments do watsonx Orchestrate via REST API."""
    try:
        api_key = os.getenv('WATSONX_API_KEY')
        url_token = 'https://iam.cloud.ibm.com/identity/token'
        
        token_data = {
            "apikey": api_key, 
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
        token_res = requests.post(url_token, data=token_data)
        token_res.raise_for_status() 
        mltoken = token_res.json()['access_token']

        url_agente = f'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{deployment_id}/ai_service?version=2021-05-01'
        
        payload = {
            "messages": [
                {"role": "user", "content": prompt_text}
            ]
        }
        
        headers_agente = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {mltoken}'
        }
        
        response = requests.post(url_agente, json=payload, headers=headers_agente)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
        
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 429:
            return "Aviso: Nossos servidores de IA estão com alta demanda no momento. Por favor, tente novamente em alguns instantes."
        return f"Erro na API da IBM: {err.response.text}"
    except Exception as e:
        return f"Erro interno na conexão com a IA: {str(e)}"

class VoluntarioListCreate(generics.ListCreateAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

class CriseListCreate(generics.ListCreateAPIView):
    queryset = Crise.objects.all().filter(ativa=True)
    serializer_class = CriseSerializer

    def perform_create(self, serializer):
        descricao_bruta = self.request.data.get('descricao_bruta')
        prompt = f"Você é um Estruturador de Crises. Extraia as necessidades urgentes deste texto e devolva de forma limpa: {descricao_bruta}"
        analise = chamar_agente_watsonx(os.getenv('ID_AGENTE_CRISE'), prompt)
        serializer.save(analise_ia=analise)

class MatchParaOngView(APIView):
    def get(self, request):
        crises = Crise.objects.filter(ativa=True)
        voluntarios = Voluntario.objects.all()
        
        if not crises.exists() or not voluntarios.exists():
            return Response({"mensagem": "Dados insuficientes para calcular match."}, status=200)

        crise_atual = crises.last() 
        lista_voluntarios = [{"id": v.id, "nome": v.nome, "habilidades": v.habilidades} for v in voluntarios]

        prompt = f"""
        Você é um Analista de Match de Voluntariado.
        Emergência Ativa: "{crise_atual.titulo}" - {crise_atual.descricao_bruta}
        Voluntários Disponíveis: {lista_voluntarios}
        
        Avalie o cenário e retorne APENAS um JSON válido (sem textos extras ou crases markdown) com os melhores perfis:
        [
            {{"voluntario_id": 1, "nome": "Nome", "score_match": "95%", "justificativa_ia": "Motivo prático..."}}
        ]
        """
        
        res_ia = chamar_agente_watsonx(os.getenv('ID_AGENTE_MATCH'), prompt)
        
        # Limpeza defensiva do JSON retornado pelo LLM
        res_ia_limpa = res_ia.replace("```json", "").replace("```", "").strip()
        
        try:
            matches_json = json.loads(res_ia_limpa)
        except:
            matches_json = [{"nome": "Resultado em Texto Bruto (IA)", "score_match": "Processado", "justificativa_ia": res_ia_limpa}]

        return Response({"crise": crise_atual.titulo, "matches": matches_json})

class MatchParaVoluntarioView(APIView):
    def get(self, request):
        crises = Crise.objects.filter(ativa=True)
        voluntarios = Voluntario.objects.all()
        
        if not crises.exists() or not voluntarios.exists():
            return Response({"mensagem": "Dados insuficientes para calcular match."}, status=200)

        voluntario_atual = voluntarios.last()
        lista_crises = [{"id": c.id, "titulo": c.titulo, "necessidade": c.descricao_bruta} for c in crises]

        prompt = f"""
        Você é um Analista de Match de Voluntariado.
        Perfil do Voluntário: {voluntario_atual.nome} | {voluntario_atual.habilidades} | {voluntario_atual.disponibilidade}
        Demandas Ativas: {lista_crises}
        
        Identifique as crises onde ele será mais útil. Retorne APENAS um JSON válido:
        [
            {{"crise_id": 1, "titulo_crise": "Título", "score_match": "88%", "como_ajudar": "Instrução..."}}
        ]
        """
        
        res_ia = chamar_agente_watsonx(os.getenv('ID_AGENTE_MATCH'), prompt)
        
        res_ia_limpa = res_ia.replace("```json", "").replace("```", "").strip()
        try:
            matches_json = json.loads(res_ia_limpa)
        except:
            matches_json = [{"titulo_crise": "Análise Bruta", "score_match": "Processado", "como_ajudar": res_ia_limpa}]

        return Response({"voluntario": voluntario_atual.nome, "matches": matches_json})

class NotificarVoluntarioView(APIView):
    def post(self, request):
        nome_voluntario = request.data.get('nome')
        crise = request.data.get('crise')
        justificativa = request.data.get('justificativa')

        prompt = f"""
        Você é um Orquestrador de Comunicação de Crises.
        A Defesa Civil convocou o voluntário {nome_voluntario} para atuar em: "{crise}".
        A justificativa foi: {justificativa}.
        Redija uma mensagem rápida, empática e urgente (como um SMS) para o celular dele.
        """
        
        res_ia = chamar_agente_watsonx(os.getenv('ID_AGENTE_COMUNICACAO'), prompt)
        return Response({"mensagem_gerada": res_ia})

class ConfirmarDisponibilidadeView(APIView):
    def post(self, request):
        nome_voluntario = request.data.get('nome')
        crise = request.data.get('crise')
        como_ajudar = request.data.get('como_ajudar')

        prompt = f"""
        Você é um Orquestrador de Comunicação. 
        O voluntário {nome_voluntario} confirmou que vai para o local da emergência: "{crise}".
        Ação prevista: {como_ajudar}.
        Escreva um log curto e direto para o painel de comando do Coordenador de Resgate, confirmando este recurso.
        """
        
        res_ia = chamar_agente_watsonx(os.getenv('ID_AGENTE_COMUNICACAO'), prompt)
        return Response({"mensagem_gerada": res_ia})