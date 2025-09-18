from pydantic import BaseModel
from typing import Optional

# Pydantic models
class ConversationMetadata(BaseModel):
    channel: Optional[str] = "web"
    language: Optional[str] = "en"
    session_id: Optional[str] = None
    timestamp: Optional[str] = None

class ProcessMessageRequest(BaseModel):
    message: str
    active_intent_id: Optional[str] = None
    conversation_metadata: Optional[ConversationMetadata] = None

class FeedbackAnalysisRequest(BaseModel):
    feedback_message: str
    target_language_code: Optional[str] = "en"