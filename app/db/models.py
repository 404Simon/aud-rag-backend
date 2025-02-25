from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum, Boolean, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.db.types import VECTOR

Base = declarative_base()

message_slide_chunk_association = Table(
    'message_slide_chunk_association',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id'), primary_key=True),
    Column('slide_chunk_id', Integer, ForeignKey('slide_chunks.id'), primary_key=True),
)

class ChatSessionStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    DONE = "done"
    ERROR = "error"

class MessageRole(str, enum.Enum):
    USER = "user"
    FILTER_PATTERNS = "filterpatterns"
    RAG_CHUNKS = "rag_chunks"

class DBChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(ChatSessionStatus), default=ChatSessionStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship(
        "DBMessage", back_populates="chat_session", order_by="DBMessage.created_at"
    )

class DBMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_session_id = Column(String, ForeignKey("chat_sessions.id"))
    text = Column(String)
    role = Column(Enum(MessageRole))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched = Column(Boolean, default=False)

    chat_session = relationship("DBChatSession", back_populates="messages")
    slide_chunks = relationship(
        "SlideChunk",
        secondary=message_slide_chunk_association,
        back_populates="messages",
    )

class SlideChunk(Base):
    __tablename__ = "slide_chunks"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    page_number = Column(Integer)
    pdf_filename = Column(String)
    embedding = Column(VECTOR)

    messages = relationship(
        "DBMessage",
        secondary=message_slide_chunk_association,
        back_populates="slide_chunks",
    )