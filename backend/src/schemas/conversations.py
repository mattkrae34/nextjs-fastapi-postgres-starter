from pydantic import BaseModel, Field
from datetime import datetime

from schemas.messages import MessageRead


class ConversationBase(BaseModel):
    pass


class ConversationCreate(ConversationBase):
    content: str
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        populate_by_name = True


class ConversationReadWithMessages(ConversationRead):
    messages: list[MessageRead]
