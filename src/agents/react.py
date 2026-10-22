from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

from langchain_core.tools import tool
import requests

@tool("get_productos",description="Get the products that the store offers and the price of each one filter by price")
def get_products():
    """Busca productos en la API de Platzi"""
    # Conexión a API
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    products = response.json()
    return "".join([f"{product['title']} - ${product['price']}\n" for product in products])



@tool("get_weather", description="Get weather for a city")
def get_weather(city: str) -> str:
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
    data = response.json()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    response = f"The weather in {city} is {data["current_weather"]["temperature"]} C with {data["current_weather"]["windspeed"]} km/h of speed "
    return response

tools = [get_products, get_weather]

model = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
)

system_prompt="""
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesitan y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda
- get_weather: para obtener el clima de la ciaudad
"""

react_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)