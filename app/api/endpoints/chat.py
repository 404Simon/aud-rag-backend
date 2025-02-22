from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas import chat as chat_schemas
from app.db.database import get_db
from app.tasks import rag_tasks
from ...core.rag.rag_pipeline import run_multi_stage_rag

router = APIRouter()

@router.post("/start", response_model=chat_schemas.StartChatResponse)
async def start_chat(
    background_tasks: BackgroundTasks,
    request: chat_schemas.StartChatRequest,
    db: Session = Depends(get_db)
):
    db_chat_session = rag_tasks.create_chat_session_db(db)
    rag_tasks.create_user_message_db(db, db_chat_session.id, request.initial_message)
    background_tasks.add_task(run_multi_stage_rag, db_chat_session.id, request.initial_message, db=db)
    return {"chat_id": db_chat_session.id}

@router.post("/{chat_id}/message", response_model=chat_schemas.SendMessageResponse)
async def send_message(chat_id: str, request: chat_schemas.SendMessageRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_chat_session = rag_tasks.get_chat_session_db(db, chat_id)
    if not db_chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    rag_tasks.create_user_message_db(db, chat_id, request.user_message)
    background_tasks.add_task(run_multi_stage_rag, chat_id, request.user_message, db=db)
    return {"status": "message received, processing"}

@router.get("/{chat_id}/poll", response_model=chat_schemas.PollResponse)
async def poll_messages(chat_id: str, db: Session = Depends(get_db)):
    db_chat_session = rag_tasks.get_chat_session_db(db, chat_id)
    if not db_chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    messages, status = rag_tasks.poll_new_messages_db(db, chat_id)
    return chat_schemas.PollResponse(messages=messages, status=status)

