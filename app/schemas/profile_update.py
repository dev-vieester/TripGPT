from pydantic import BaseModel

class ProfileUpdateRequest(BaseModel):
    field: str | None = None