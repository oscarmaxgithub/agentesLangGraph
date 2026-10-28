from email import message
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

load_dotenv()

from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from src.agents.support.agent import agent

app = FastAPI()


class Message(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# @app.post("/chat/{chat_id}")
# async def chat(chat_id: str, item: Message, checkpointer: CheckpointerDep):
#     # CRUD add message
#     config = {
#         "configurable": {
#             "thread_id": chat_id,
#         }
#     }
#     human_message = HumanMessage(content=item.message)
#     agent = make_graph(config={"checkpointer": checkpointer})
#     state = {"messages": [human_message]}
#     response = agent.invoke(state, config)
#     last_message = response["messages"][-1]
#     # CRUD add message
#     return response["messages"]


##Endpoint de tipo servlet
@app.post("/chat/{chat_id}")
async def chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)
    response = agent.invoke({"messages": [human_message]})
    last_message = response["messages"][-1]
    return last_message.text
    
##Endpoint de tipo Stream
@app.post("/chat/{chat_id}/stream")
async def stream_chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)
    async def generate_response():
        for menssage_chunk, metadata in agent.stream({"messages":[human_message]}, stream_mode="messages"):
            if menssage_chunk.content:
                yield f"data: {menssage_chunk.content}\n\n"
        
        print(menssage_chunk.content, end="|", flush=True)
    return StreamingResponse(generate_response(),media_type="text/event-stream")


