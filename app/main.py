from fastapi import FastAPI
from app.api import routers
from app.db.database import create_database_tables

app = FastAPI()

app.include_router(routers.chat_router, prefix="/chat", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    create_database_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
