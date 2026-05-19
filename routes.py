from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from chat import send_message_to_ai, reset_chat

router = APIRouter()

class User_message(BaseModel):
    message: str = Field(...)

@router.post("/send_message")
async def invoke(item: User_message):
    def stream():
        for chunk in send_message_to_ai(item.message):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(stream(), media_type="text/event-stream")
    

@router.post("/reset")
async def reset():
    reset_chat()
    return {"status": "ok"}