from pydantic import BaseModel
from typing import List

class SlideChunkOut(BaseModel):
    id: int
    content: str
    page_number: int
    pdf_filename: str

class Message(BaseModel):
    text: str
    role: str
    similar_chunks: List[SlideChunkOut] = []

class StartChatRequest(BaseModel):
    initial_message: str

class StartChatResponse(BaseModel):
    chat_id: str

class SendMessageRequest(BaseModel):
    user_message: str

class SendMessageResponse(BaseModel):
    status: str

class PollResponse(BaseModel):
    messages: List[Message]
    status: str