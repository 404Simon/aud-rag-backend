from fastapi import APIRouter
from app.api.endpoints import chat

chat_router = APIRouter()
chat_router.include_router(chat.router)
