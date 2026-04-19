# CRIACAO-API-PARA-BOT-WHATSAPP

# 🌡️ API Clima + WhatsApp Bot

API em FastAPI que busca dados climáticos em tempo real e envia notificações formatadas via WhatsApp usando o serviço CallMeBot.

---

## 📋 Funcionalidades

- Busca temperatura, sensação térmica, chuva e período do dia (dia/noite) pela API Open-Meteo
- Salva os dados em banco SQLite local
- Envia mensagem formatada com emojis para o WhatsApp via CallMeBot
- Agendamento automático com APScheduler (opcional)

---

## 🗂️ Estrutura do Projeto


API_PREÇO_WHATSAPP/
├── main.py                        # FastAPI + endpoints + agendamento
├── sql.py                         # Banco de dados SQLite
├── banco.db                       # Arquivo gerado automaticamente
├── .env                           # Variáveis de ambiente (não versionar)
├── formatacao/
│   ├── __init__.py
│   └── mensagemFormatada.py       # Formatação da mensagem do WhatsApp
└── services/
    ├── __init__.py
    └── weather_service.py         # Integração com Open-Meteo


---

## ⚙️ Instalação

*1. Clone o projeto e entre na pasta:*
bash
cd API_PREÇO_WHATSAPP


*2. Crie e ative o ambiente virtual:*
bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac


*3. Instale as dependências:*
bash
pip install fastapi uvicorn httpx openmeteo-requests requests-cache retry-requests python-dotenv apscheduler


---

## 🔑 Configuração

Antes de rodar, configure as variáveis no main.py:

python
LAT, LONG = -15.xxxx, -59.xxxx   # Suas coordenadas

MEU_NUMERO = "55XXXXXXXXXXX"      # Seu número com DDI + DDD
API_KEY    = "XXXXXXX"            # Chave gerada pelo CallMeBot


### Como obter a API Key do CallMeBot

1. Adicione o contato *+34 644 28 79 90* no WhatsApp
2. Envie a mensagem: I allow callmebot to send me messages
3. Aguarde a resposta com sua apikey

---

## ▶️ Como Rodar

bash
uvicorn main:app --reload


Acesse a documentação interativa em:

http://127.0.0.1:8000/docs


---

## 🚀 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /meu-clima/ | Busca o clima atual e salva no banco |
| POST | /mandar-zap/ | Envia o último clima salvo para o WhatsApp |

### Exemplo de resposta — /meu-clima/
json
{
  "id": 1,
  "dados": {
    "temp": 26.2,
    "feels_like": 31.1,
    "is_day": false,
    "rain": 0
  }
}


### Mensagem recebida no WhatsApp

🌡️ Clima Atual
──────────────
📍 Lat: -15.2261 | Lon: -59.3353
🕐 Horário: 2026-04-19 20:18:48
🌡️ Temperatura: 26.2°C
🤔 Sensação: 31.1°C (😓 Quente)
🌧️ Chuva: Sem chuva 🌤️
🌓 Período: 🌙 Noite


---

## ⏰ Agendamento Automático (Opcional)

Para receber o clima automaticamente todo dia às 7h, adicione ao main.py:

python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="America/Cuiaba")

@app.on_event("startup")
async def startup_event():
    init_db()
    scheduler.add_job(meu_clima,   "cron", hour=7, minute=0)
    scheduler.add_job(mandar_zap,  "cron", hour=7, minute=2)
    scheduler.start()


---

## 🗄️ Banco de Dados

A tabela weather é criada automaticamente no primeiro start:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| latitude | REAL | Latitude consultada |
| longitude | REAL | Longitude consultada |
| temp | REAL | Temperatura em °C |
| feels_like | REAL | Sensação térmica em °C |
| is_day | INTEGER | 1 = dia, 0 = noite |
| rain | REAL | Chuva em mm |
| fetched_at | TEXT | Data/hora do registro |

---

## 🛠️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — Framework web
- [Open-Meteo](https://open-meteo.com/) — API de clima gratuita
- [CallMeBot](https://www.callmebot.com/) — Envio de WhatsApp
- [SQLite](https://www.sqlite.org/) — Banco de dados local
- [APScheduler](https://apscheduler.readthedocs.io/) — Agendamento de tarefas
- [httpx](https://www.python-httpx.org/) — Requisições HTTP assíncronas

---

## 📄 Licença

Projeto pessoal para fins de estudo e automação residencial.
