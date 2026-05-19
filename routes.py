from fastapi import APIRouter
from pydantic import BaseModel, Field
from chat import send_message_to_ai

router = APIRouter()

class User_message(BaseModel):
    message: str = Field(...)

@router.post("/send_message")
async def invoke(item: User_message):
    response = send_message_to_ai(item.message)
    return {"reply": response}
    