

from langchain.chat_models import init_chat_model
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

from src.agents.support.nodes.extractor.prompt import SYSTEM_PROMPT_EXTRACTOR
from src.agents.support.state import State

# llmOpenRouter = ChatOpenRouter(
#     model="openrouter/free",
#     temperature=1,
# )
llm = init_chat_model("openai:gpt-4o", temperature=0)

## Clase para schema
class ContactInfo(BaseModel):
    """ Contact information for a person """
    name: str =  Field(description= "The name of the person")
    email: str =  Field(description= "The email of the person")
    phone: str =  Field(description= "The phone number of the person")
    # tone: int = Field(description="The tone of the person", ge=0, le=100)
    age: str = Field(description="The tone of the person")
    # sentiment: str =  Field(description= "The sentiment convertation of the person")

llm = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name:str = state.get("customer_name", None)
    new_state:State ={}
    if customer_name is None or len(history)>=10 :
        #Obtengo el historial del chat
        schema = llm.invoke(
            [("system",SYSTEM_PROMPT_EXTRACTOR)]+ history
        )
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        # new_state["tone"] = schema.tone
        new_state["age"] = schema.age

    return new_state



