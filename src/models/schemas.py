from pydantic import BaseModel
from typing import Optional

# Pydantic models
class ConversationMetadata(BaseModel):
    channel: str = "web"
    language: str = "en"
    session_id: str = None
    timestamp: Optional[str] = None

class ProcessMessageRequest(BaseModel):
    message: str
    active_intent_id: Optional[str] = None
    conversation_metadata: ConversationMetadata = None

class FeedbackAnalysisRequest(BaseModel):
    feedback_message: str
    target_language_code: str = "en"