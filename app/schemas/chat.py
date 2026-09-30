from pydantic import BaseModel, Field
from typing import Any

class StartChatResponse(BaseModel):
    message:str = Field(
        min_length=1,
        description="The traveller's first message"
    )

class ContinueChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        description="The traveller's next message"
    )

class ChatResponse(BaseModel):
    thread_id: str
    status: str
    message: str
    missing_field: list[str] = Field(default_factory=list)
    trip_profile: dict[str, Any] | None = None
