from sqlalchemy.orm import Session
from app.db import models
from app.db.models import ChatSessionStatus
import asyncio

async def run_multi_stage_rag(chat_session_id: str, user_message: str, db: Session):
    db_chat_session = db.query(models.DBChatSession).filter(models.DBChatSession.id == chat_session_id).first()
    if not db_chat_session:
        print(f"Chat session {chat_session_id} not found in RAG task.")
        return

    db_chat_session.status = ChatSessionStatus.GENERATING
    db.commit()

    try:
        await asyncio.sleep(1)
        db_message1 = models.DBMessage(chat_session_id=chat_session_id, text="Stage 1 of response...", is_user=False)
        db.add(db_message1)
        db.commit()

        await asyncio.sleep(2)
        db_message2 = models.DBMessage(chat_session_id=chat_session_id, text="Stage 2 with more details...", is_user=False)
        db.add(db_message2)
        db.commit()

        await asyncio.sleep(1)
        db_message3 = models.DBMessage(chat_session_id=chat_session_id, text="Final stage of response. Done.", is_user=False)
        db.add(db_message3)
        db.commit()

        db_chat_session.status = ChatSessionStatus.DONE
        db.commit()

    except Exception as e:
        print(f"Error in RAG task for session {chat_session_id}: {e}")
        db_chat_session.status = ChatSessionStatus.ERROR
        db.commit()
