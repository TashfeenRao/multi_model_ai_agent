from fastapi import FastAPI, HTTPException
from app.common.logger import get_logger
from app.core.ai_agent import get_response_from_ai_agent
from pydantic import BaseModel
from app.config.settings import settings

logger = get_logger(__name__)


app = FastAPI()


class ChatRequest(BaseModel):
    model: str
    query: str
    allow_search: bool
    system_prompt: str


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logger.info(f"Chat request received: {request}")
        if request.model not in settings.ALLOWED_MODELS:
            raise HTTPException(
                status_code=400, detail=f"Invalid model: {request.model}")

        logger.info(f"Getting response from AI agent: {request.model}")

        return {"message": get_response_from_ai_agent(request.model, request.query,
                                                      request.allow_search, request.system_prompt)}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error in chat: {e}")
