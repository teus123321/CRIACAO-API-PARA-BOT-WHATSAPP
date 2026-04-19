# formatacao/mensagemFormatada.py

def formatar_mensagem_clima(dados: tuple) -> str:
    if not dados:
        return "⚠️ Nenhum dado climático disponível."

    id_, lat, lon, temp, feels_like, is_day, rain, fetched_at = dados

    periodo = "☀️ Dia" if is_day else "🌙 Noite"
    chuva = f"{rain:.1f} mm" if rain > 0 else "Sem chuva 🌤️"
    sensacao = (
        "🥵 Muito quente" if feels_like >= 35 else
        "😓 Quente"       if feels_like >= 28 else
        "😊 Agradável"    if feels_like >= 18 else
        "🧥 Frio"         if feels_like >= 10 else
        "🥶 Muito frio"
    )

    return (
        f"🌡️ *Clima Atual*\n"
        f"──────────────\n"
        f"📍 Lat: {lat:.4f} | Lon: {lon:.4f}\n"
        f"🕐 Horário: {fetched_at}\n"
        f"🌡️ Temperatura: {temp:.1f}°C\n"
        f"🤔 Sensação: {feels_like:.1f}°C ({sensacao})\n"
        f"🌧️ Chuva: {chuva}\n"
        f"🌓 Período: {periodo}"
    )