def get_weather(city: str) -> dict:
    cities = {
        "delhi": {"temp": 28, "condition": "Partly Cloudy"},
        "mumbai": {"temp": 30, "condition": "Humid"},
        "kolkata": {"temp": 32, "condition": "Sunny"}
    }
    return cities.get(city.lower(), {"temp": 25, "condition": "Clear"})

def search_web(query: str) -> str:
    if "climate" in query.lower():
        return "Climate change is a long-term shift in global weather patterns."
    elif "ai" in query.lower():
        return "AI is the simulation of human intelligence in machines."
    else:
        return f"Information about {query}"