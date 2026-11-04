import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from langgraph.checkpoint.postgres import PostgresSaver

# DB_URI = os.getenv("DB_URI")
DB_URI = "postgresql://postgres:postgres@localhost:5433/my_course_agent"

# Global checkpointer instance
_checkpointer: PostgresSaver | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _checkpointer
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        _checkpointer = checkpointer
        _checkpointer.setup()
        yield


def get_checkpointer() -> PostgresSaver:
    if _checkpointer is None:
        raise RuntimeError(
            "Checkpointer no inicializado. Make sure lifespan is running."
        )
    return _checkpointer


CheckpointerDep = Annotated[PostgresSaver, Depends(get_checkpointer)]
