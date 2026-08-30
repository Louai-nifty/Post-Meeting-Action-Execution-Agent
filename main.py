from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from routers import webhooks
from agent.graph import graph
import asyncio
from utils.loggings import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string("checkpoints_data/checkpoints.db") as checkpointer:
        app.state.agent = graph.compile(
            checkpointer=checkpointer,
            interrupt_before=[""],
            interrupt_after=[""]
        )
        yield

app = FastAPI(
    title="Post-Meeting-Action-Execution-Agent",
    description="End-to-end meeting automation pipeline with human-in-the-loop approval",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(webhooks.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Post-Meeting-Action-Execution-Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)