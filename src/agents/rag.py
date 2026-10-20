import random
from dotenv import load_dotenv
from langchain_core.runnables import history
from langchain.chat_models import init_chat_model
from langgraph.graph import  MessagesState, StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_openrouter import ChatOpenRouter


load_dotenv()
llmOpenAI = init_chat_model("openai:gpt-4o", temperature=0)
llmOpenRouter = ChatOpenRouter(
    model="openrouter/free",
    temperature=1,
)

#Declaro un arreglo de ID donde esta mi RAG en OpenAI
openai_vector_store_ids=[
    "vs_6ad697ce3b0c81918cad194beb70a4a4"
]
#Declaro la tool a usar propias de OpenAI
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids
}

llmOpenAI =llmOpenAI.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    phone: str
    my_age: str


class ContactInfo(BaseModel):
    """ Contact information for a person """
    name: str =  Field(description= "The name of the person")
    email: str =  Field(description= "The email of the person")
    phone: str =  Field(description= "The phone number of the person")
    # tone: int = Field(description="The tone of the person", ge=0, le=100)
    age: str = Field(description="The tone of the person")
    # sentiment: str =  Field(description= "The sentiment convertation of the person")



llm_with_strutured_output = llmOpenRouter.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name:str = state.get("customer_name", None)
    new_state:State ={}
    if customer_name is None or len(history)>=10 :
        #Obtengo el historial del chat
        schema = llm_with_strutured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        # new_state["tone"] = schema.tone
        new_state["age"] = schema.age

    return new_state

def conversation(state:State):
    new_state: State={}
    history = state["messages"]
    last_message = history[-1]
    customer_name= state.get("customer_name","Jhon Doe")
    system_message=f"You are a helpful assitant that can answer questions about the customer {customer_name} "
    ai_message = llmOpenAI.invoke([
        ("system",system_message),
        ("user",last_message.text)
    ])
    new_state["message"] = [ai_message]
    return new_state

builder = StateGraph(State)
builder.add_node("conversation",conversation)
builder.add_node("extractor",extractor)

builder.add_edge(START,"extractor")
builder.add_edge("extractor","conversation")
builder.add_edge("conversation",END)

agent = builder.compile()

