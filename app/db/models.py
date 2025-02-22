from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()

class ChatSessionStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    DONE = "done"
    ERROR = "error"

class DBChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(ChatSessionStatus), default=ChatSessionStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship("DBMessage", back_populates="chat_session", order_by="DBMessage.created_at")

class DBMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_session_id = Column(String, ForeignKey("chat_sessions.id"))
    text = Column(String)
    is_user = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched = Column(Boolean, default=False)

    chat_session = relationship("DBChatSession", back_populates="messages")
