# pip install -qU langchain "langchain[openai]"
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )
# print(result["messages"][-1].content_blocks)
