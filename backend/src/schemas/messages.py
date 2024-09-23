from datetime import datetime
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    conversation_id: int = Field(alias="conversationId")
    timestamp: datetime

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        populate_by_name = True
