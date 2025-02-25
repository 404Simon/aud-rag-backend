from sqlalchemy.orm import Session
from app.db import models
from app.schemas import chat as chat_schemas


def create_chat_session_db(db: Session) -> models.DBChatSession:
    db_chat_session = models.DBChatSession()
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)
    return db_chat_session


def get_chat_session_db(db: Session, chat_id: str) -> models.DBChatSession | None:
    return (
        db.query(models.DBChatSession)
        .filter(models.DBChatSession.id == chat_id)
        .first()
    )


def create_user_message_db(
    db: Session, chat_session_id: str, user_message: str
) -> models.DBMessage:
    db_user_message = models.DBMessage(
        chat_session_id=chat_session_id,
        text=user_message,
        role=models.MessageRole.USER,
    )
    db.add(db_user_message)
    db.commit()
    return db_user_message


def poll_new_messages_db(
    db: Session, chat_id: str
) -> tuple[list[chat_schemas.Message], models.ChatSessionStatus]:
    db_chat_session = get_chat_session_db(db, chat_id)
    if not db_chat_session:
        return [], models.ChatSessionStatus.ERROR

    db_new_messages = (
        db.query(models.DBMessage)
        .filter(
            models.DBMessage.chat_session_id == chat_id,
            # models.DBMessage.fetched == False # always return all messages for now
        )
        .order_by(models.DBMessage.created_at)
        .all()
    )

    messages_to_return = []
    for db_message in db_new_messages:
        messages_to_return.append(
            chat_schemas.Message(text=db_message.text, role=db_message.role)
        )
        db_message.fetched = True
    db.commit()

    return messages_to_return, db_chat_session.status
