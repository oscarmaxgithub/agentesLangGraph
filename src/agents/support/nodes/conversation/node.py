from langchain.chat_models import init_chat_model

from src.agents.support.nodes.conversation.prompt import SYSTEM_PROMPT_CONVERSATION
from src.agents.support.nodes.conversation.tools import tools
from src.agents.support.state import State

llmOpenAI = init_chat_model("openai:gpt-4o", temperature=0)


llmOpenAI =llmOpenAI.bind_tools(tools)


def conversation(state:State):
    new_state: State={}
    history = state["messages"]
    last_message = history[-1]
    ai_message = llmOpenAI.invoke([
        ("system",SYSTEM_PROMPT_CONVERSATION),
        ("user",last_message.text)
    ])
    new_state["messages"] = [ai_message]
    return new_state