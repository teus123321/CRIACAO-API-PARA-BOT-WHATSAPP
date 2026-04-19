from formatacao.mensagemFormatada import formatar_mensagem_clima
import logging
from sql import init_db, insert_weather, get_last_weather
from services.weather_service import fetch_current_weather
from fastapi import FastAPI, HTTPException, logger
from pydantic import BaseModel
import httpx
import urllib.parse
from dotenv import load_dotenv

#variáveis de ambiente para configuração (ex: número e chave de API para CallMeBot)
load_dotenv()

# Configuração de logging que é importante para monitorar o comportamento da aplicação e diagnosticar problemas
logger = logging.getLogger(__name__)

# Configuração básica de logging
app = FastAPI(title ="API de Teste")

# Evento de inicialização para criar a tabela no banco de dados se ela não existir
@app.on_event("startup")
async def startup_event():
    init_db()

# Coordenadas para teste (exemplo: Cuiabá, MT)
LAT, LONG= -15.xxxx, -59.xxxx  # Exemplo de coordenadas para teste= -15.2261, -59.3353  # Exemplo de coordenadas para teste

#número e chave de API para o serviço de envio de mensagens (CallMeBot)
MEU_NUMERO = "xxxxxxxxxxx"  # Substitua pelo seu número de telefone com código do país, ex: 5511999999999
API_KEY = "xxxxxxxxxxxxxxxxxxxx"  # Substitua pela sua chave de API do CallMeBot


class Notificacao(BaseModel):
    mensagem: str

# Endpoint para obter o clima atual e salvar no banco de dados
@app.get("/meu-clima/")
async def meu_clima(lat: float = LAT, long: float = LONG):

    #buscar os dadoas climáticos atuais usando a função fetch_current_weather
    try:
        dados = await fetch_current_weather(lat, long)
    except TimeoutError as e:
        logger.error("Timeout ao buscar clima: %s", e)
        raise HTTPException(status_code=504, detail="Serviço de clima indisponível")
    except ConnectionError as e:
        logger.error("Erro de conexão ao buscar clima: %s", e)
        raise HTTPException(status_code=502, detail="Falha na conexão com serviço externo")
    except Exception as e:
        logger.exception("Erro inesperado ao buscar clima")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

    if not dados:
        raise HTTPException(status_code=404, detail="Dados climáticos não encontrados")
    
    #salvar os dados climáticos no banco de dados usando a função insert_weather
    try:
        row_id =(
                insert_weather(
                    lat, long, 
                    dados["temp"], 
                    dados["feels_like"], 
                    dados["is_day"], 
                    dados["rain"]
                )
        )
        insert_weather(lat, long, dados["temp"], dados["feels_like"], dados["is_day"], dados["rain"])
    except KeyError as e:
        logger.error("Campo ausente nos dados climáticos: %s", e)
        raise HTTPException(status_code=422, detail=f"Dado inválido: campo {e} ausente")
    except Exception as e:
        logger.exception("Erro ao salvar dados climáticos no banco")
        raise HTTPException(status_code=500, detail="Erro ao persistir dados")
    
    #retornar o ID do registro inserido e os dados climáticos
    return {
        "id" : row_id,
        "dados" : dados
    }
        
# Endpoint para enviar a mensagem formatada para o WhatsApp usando CallMeBot
@app.post("/mandar-zap/")
async def mandar_zap():

    #recuperar os dados climáticos mais recentes do banco de dados usando a função get_last_weather
    try:
        dados = get_last_weather(LAT, LONG)
    except Exception as e:
        logger.error("Erro ao recuperar dados climáticos: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao recuperar dados climáticos")

    mensagem = formatar_mensagem_clima(dados)

    #construir a URL para enviar a mensagem usando CallMeBot
    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={MEU_NUMERO}"
        f"&text={urllib.parse.quote(mensagem)}"
        f"&apikey={API_KEY}"
    )

    #enviar a mensagem para CallMeBot usando httpx e lidar com possíveis erros de rede ou resposta
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
    except httpx.TimeoutException:
        logger.error("Timeout ao enviar mensagem para CallMeBot")
    except httpx.RequestError as e:
        logger.error("Erro de conexão com CallMeBot: %s", e)
        raise HTTPException(status_code=502, detail="Falha na conexão com CallMeBot")
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"CallMeBot retornou {response.status_code}: {response.text}"
        )
    
    #logar o sucesso do envio da mensagem para monitoramento e depuração
    logger.info("Mensagem enviada com sucesso para %s", MEU_NUMERO)
    return {
        "message": "Mensagem enviada com sucesso!",
        "preview": mensagem  # útil para depuração
    }
