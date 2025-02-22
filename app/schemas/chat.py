from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    text: str
    is_user: bool

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
