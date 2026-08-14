from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str = Field(..., description="Usually 'user', 'assistant', or 'system'")
    content: str = Field(..., description="The actual content of the message")

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the user session")
    messages: list[Message] = Field(..., description="The conversation history")
    model: str = Field(..., description="The requested model")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    