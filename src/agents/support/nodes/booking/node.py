from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

from src.agents.support.nodes.booking.prompt import prompt_template
from src.agents.support.nodes.booking.tools import tools

model = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
)

booking_node = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt_template.format()
)