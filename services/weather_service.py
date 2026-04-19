import openmeteo_requests
import requests_cache
from retry_requests import retry

# Configuração global de cache e retry (fora da função para persistir entre chamadas)
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

async def fetch_current_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "apparent_temperature", "is_day", "rain"],
        "timezone": "auto"
    }
    
    # Nota: weather_api é síncrona na lib oficial, 
    # em produção pesada usaríamos um executor para não bloquear o loop do FastAPI
    responses = openmeteo.weather_api(url, params=params)
    res = responses[0]
    current = res.Current()
    
    return {
        "temp": round(current.Variables(0).Value(), 1),
        "feels_like": round(current.Variables(1).Value(), 1),
        "is_day": bool(current.Variables(2).Value()),
        "rain": current.Variables(3).Value()
    }