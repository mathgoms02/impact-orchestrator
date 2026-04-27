# 🤝 Impact Orchestrator

![Badge](https://img.shields.io/badge/Status-MVP-brightgreen)
![Hackathon](https://img.shields.io/badge/Hackathon26-UNASP-blue)
![Tech](https://img.shields.io/badge/AI-IBM_watsonx-0f62fe)

Plataforma desenvolvida para otimizar e orquestrar a alocação de voluntários em situações de crise e desastres naturais, utilizando Inteligência Artificial para análise de perfil e comunicação em tempo real.

## 📺 Vídeo de Demonstração

Confira a apresentação completa da solução e as funcionalidades em operação:
👉 [Assista ao vídeo no Google Drive](https://drive.google.com/file/d/1rbYigVBVMe6TLDxsGRAvrpbPFnI1xK2Y/view?usp=sharing)

## 💡 O Problema

Durante emergências, o grande desafio das ONGs não é a falta de voluntários, mas a desorganização e a dificuldade de alocar rapidamente as pessoas certas para as necessidades mais urgentes. A triagem manual custa tempo, e em crises, tempo é vida.

## 🚀 A Solução

Um sistema inteligente de duplo painel (Instituições e Voluntários). O Impact Orchestrator utiliza microsserviços de IA para ler as demandas emergenciais em linguagem natural, analisar o banco de voluntários e realizar um "Match" perfeito baseado em habilidades e disponibilidade, gerando comunicações automáticas de convocação.

## 🛠️ Tecnologias Utilizadas

- **Frontend:** React (Vite), CSS Grid, Axios, JWT Decode.
- **Backend:** Python, Django REST Framework, SimpleJWT.
- **Inteligência Artificial:** IBM watsonx.ai (Modelos Granite/Llama via API REST).
- **Arquitetura:** Integração baseada em Deployments Específicos (Agentes de Match, Estruturação de Crise e Comunicação).

## ⚙️ Como Executar o Projeto

### Pré-requisitos

- Node.js instalado.
- Python 3.10+ instalado.
- Conta ativa na IBM Cloud com API Key gerada.

### 1. Configurando o Backend (Django)

Navegue até a pasta do backend:

```bash
cd backend
```

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt requests python-dotenv
```

Configure as variáveis de ambiente criando um arquivo `.env` na raiz do backend:

```env
WATSONX_API_KEY=sua_api_key_da_ibm
WATSONX_PROJECT_ID=seu_project_id
ID_AGENTE_MATCH=seu_deployment_id_de_match
ID_AGENTE_CRISE=seu_deployment_id_de_crise
ID_AGENTE_COMUNICACAO=seu_deployment_id_de_comunicacao
```

Rode as migrações e inicie o servidor:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. Configurando o Frontend (React)

Em um novo terminal, navegue até a pasta do frontend:

```bash
cd frontend
```

Instale as dependências e inicie o servidor de desenvolvimento:

```bash
npm install
npm run dev
```

Acesse a aplicação no navegador através do endereço `http://localhost:5173`.

## 🧠 Como a Integração com watsonx Funciona

A aplicação não utiliza chamadas genéricas de LLM. Os fluxos de IA foram arquitetados utilizando Deployments dedicados na plataforma watsonx.ai. O backend em Django atua como um maestro, autenticando-se via IAM Token e disparando payloads específicos para cada "Agente" (Analista de Match, Orquestrador de Comunicação), garantindo respostas formatadas em JSON estruturado para o React.
