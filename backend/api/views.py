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
import json
from google.genai import types
from dotenv import load_dotenv

from google import genai

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
        # Inicializa o cliente com a nova estrutura da API
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Injeção de contexto baseada no ID do agente (Mantendo a "magia")
        contexto_adicional = ""
        if deployment_id == os.getenv('ID_AGENTE_MATCH'):
            contexto_adicional = "Você é um Analista de Match de Voluntariado. Responda APENAS com a Função Recomendada, Score de Match e Justificativa. "
        elif deployment_id == os.getenv('ID_AGENTE_CRISE'):
            contexto_adicional = "Você é um Estruturador de Crises. Extraia as necessidades urgentes deste texto e devolva de forma limpa e direta. "
        elif deployment_id == os.getenv('ID_AGENTE_COMUNICACAO'):
            contexto_adicional = "Você é um Orquestrador de Comunicação. Escreva uma mensagem urgente, empática e profissional para convocar o voluntário. "

        prompt_final = contexto_adicional + prompt_text
        
        # Nova sintaxe de chamada usando o modelo mais recente e rápido
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_final
        )
        
        return response.text
        
    except Exception as e:
        return f"Erro na IA (Magia do Cinema falhou): {str(e)}"


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


class MatchParaOngView(APIView):
    def get(self, request):
        # 1. Pega todas as crises ativas e todos os voluntários
        crises = Crise.objects.filter(ativa=True)
        voluntarios = Voluntario.objects.all()
        
        if not crises.exists() or not voluntarios.exists():
            return Response({"mensagem": "Faltam dados (crises ou voluntários) para o match."}, status=200)

        # Vamos usar a última crise registrada para o demo
        crise_atual = crises.last() 
        lista_voluntarios = [{"id": v.id, "nome": v.nome, "habilidades": v.habilidades} for v in voluntarios]

        prompt = f"""
        Você é um Orquestrador de IA. 
        Temos esta emergência: "{crise_atual.titulo}" - {crise_atual.descricao_bruta}
        Temos estes voluntários: {lista_voluntarios}
        
        Analise quem pode ajudar. Retorne uma lista com os melhores matches.
        A resposta DEVE obedecer exatamente este esquema JSON, sem nenhum outro texto:
        [
            {{"voluntario_id": 1, "nome": "Nome", "score_match": "95%", "justificativa_ia": "Motivo prático..."}}
        ]
        """

        try:
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", # Força a IA a cuspir JSON perfeito!
                ),
            )
            return Response({"crise": crise_atual.titulo, "matches": json.loads(response.text)})
        except Exception as e:
            return Response({"erro": str(e)}, status=500)

class MatchParaVoluntarioView(APIView):
    def get(self, request):
        crises = Crise.objects.filter(ativa=True)
        voluntarios = Voluntario.objects.all()
        
        if not crises.exists() or not voluntarios.exists():
            return Response({"mensagem": "Faltam dados para o match."}, status=200)

        # Pega o último voluntário cadastrado para o demo
        voluntario_atual = voluntarios.last()
        lista_crises = [{"id": c.id, "titulo": c.titulo, "necessidade": c.descricao_bruta} for c in crises]

        prompt = f"""
        Você é um Orquestrador de IA.
        Temos este voluntário: {voluntario_atual.nome} com as habilidades: {voluntario_atual.habilidades} e disponibilidade: {voluntario_atual.disponibilidade}.
        Temos estas crises ativas: {lista_crises}
        
        Quais crises se encaixam no perfil dele? Retorne uma lista JSON com os melhores matches:
        [
            {{"crise_id": 1, "titulo_crise": "Nome", "score_match": "88%", "como_ajudar": "Instrução prática..."}}
        ]
        """

        try:
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            return Response({"voluntario": voluntario_atual.nome, "matches": json.loads(response.text)})
        except Exception as e:
            return Response({"erro": str(e)}, status=500)

class NotificarVoluntarioView(APIView):
    def post(self, request):
        nome_voluntario = request.data.get('nome')
        crise = request.data.get('crise')
        justificativa = request.data.get('justificativa')

        # Prompt focado na comunicação ONG -> Voluntário
        prompt = f"""
        Você é o Orquestrador de Comunicação da plataforma.
        A ONG acabou de selecionar o voluntário {nome_voluntario} para a emergência: "{crise}".
        O motivo da escolha foi: {justificativa}.
        
        Redija uma mensagem curta (estilo WhatsApp), urgente, empática e muito profissional para avisar o voluntário que precisamos dele. Não mencione pagamentos.
        """

        try:
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return Response({"mensagem_gerada": response.text})
        except Exception as e:
            return Response({"erro": str(e)}, status=500)

class ConfirmarDisponibilidadeView(APIView):
    def post(self, request):
        nome_voluntario = request.data.get('nome')
        crise = request.data.get('crise')
        como_ajudar = request.data.get('como_ajudar')

        # Prompt focado na comunicação Voluntário -> ONG
        prompt = f"""
        Você é o Orquestrador de Comunicação da plataforma.
        O voluntário {nome_voluntario} acabou de confirmar que está a caminho para ajudar na emergência: "{crise}".
        Ele vai atuar fazendo o seguinte: {como_ajudar}.
        
        Redija um alerta muito curto e objetivo (estilo notificação de sistema operacional) para o Coordenador da ONG, avisando que o voluntário confirmou presença e o que ele fará.
        """

        try:
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return Response({"mensagem_gerada": response.text})
        except Exception as e:
            return Response({"erro": str(e)}, status=500)