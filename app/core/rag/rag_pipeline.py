from sqlalchemy.orm import Session
from app.db import models
from app.db.models import ChatSessionStatus
from app.core.rag.relevant_topics import find_relevant_topics, RelevantTopics
from app.core.rag.vectorstore import query_similar_chunks
import asyncio


async def run_multi_stage_rag(chat_session_id: str, user_message: str, db: Session):
    db_chat_session = (
        db.query(models.DBChatSession)
        .filter(models.DBChatSession.id == chat_session_id)
        .first()
    )
    if not db_chat_session:
        print(f"Chat session {chat_session_id} not found in RAG task.")
        return

    db_chat_session.status = ChatSessionStatus.GENERATING
    db.commit()

    relevant_topics: RelevantTopics = find_relevant_topics(user_message).parsed
    filter_patterns = relevant_topics.get_document_title_filterpatterns()
    filter_patterns_message = models.DBMessage(
        chat_session_id=chat_session_id,
        text=f"Filterpatterns: {str(filter_patterns)}",
        role=models.MessageRole.FILTER_PATTERNS,
    )
    db.add(filter_patterns_message)
    db.commit()

    similar_chunks = query_similar_chunks(
        db,
        user_message,
        top_k=5,
        document_title_filter_patterns=filter_patterns,
    )

    similar_chunks_message = models.DBMessage(
        chat_session_id=chat_session_id,
        text="Similar chunks attached",
        role=models.MessageRole.RAG_CHUNKS,
    )
    db.add(similar_chunks_message)
    db.commit()

    for chunk in similar_chunks:
        similar_chunks_message.slide_chunks.append(chunk)
    db.commit()

    db_chat_session.status = ChatSessionStatus.DONE
    db.commit()