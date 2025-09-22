from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import logging
from typing import Optional, Dict, Any

from src.services.intent_service import intent_service
from src.services.feedback_service import feedback_service
from src.config.settings import settings
from src.models.schemas import ConversationMetadata, ProcessMessageRequest, FeedbackAnalysisRequest
from src.utils.auth import verify_api_key

# Initialize FastAPI app
app = FastAPI(title="Chatbot AI", version="1.0.0")

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@app.post("/v1/chatbot-ai/feedback-analysis")
async def analyze_feedback(
    request: FeedbackAnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze sentiment of customer feedback message.
    Returns sentiment, translation, and keywords.
    """
    try:
        feedback_message = request.feedback_message.strip()
        if not feedback_message:
            raise HTTPException(status_code=400, detail="Feedback message is required")

        target_language = request.target_language_code or "en"

        logger.info(f"Analyzing sentiment for feedback: {feedback_message[:50]}...")
        logger.info(f"Target language: {target_language}")

        # Process sentiment analysis
        result = await feedback_service.analyze_feedback(feedback_message, target_language)

        # Check for errors
        if result.get("status") == "Error":
            raise HTTPException(status_code=500, detail=result.get("error", "Sentiment analysis failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/v1/chatbot-ai/intent-entity-detection")
async def intent_entity_detection(
    request: ProcessMessageRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Process user message - classify intent and extract fields.
    Returns entities with user_input field populated (no response field).
    """
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        logger.info(f"Processing message: {message}")
        logger.info(f"Active intent: {request.active_intent_id}")

        result = await intent_service.process_message(message, request.active_intent_id)

        # Check for errors
        if result.get("status") == "Error":
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint - no authentication required."""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "service": "chatbot-ai",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint - no authentication required."""
    return {
        "message": "Chatbot AI Service",
        "version": "1.0.0",
        "status": "Running"
    }


@app.post("/v1/chatbot-ai/validate-entities")
async def validate_entities_endpoint(
    entities: list,
    api_key: str = Depends(verify_api_key)
):
    """
    Endpoint to validate entity structure and ensure proper format.
    """
    try:
        # Simple validation for the new structure
        validated = []
        for entity in entities:
            if isinstance(entity, dict):
                clean_entity = {
                    'id': entity.get('id', ''),
                    'label': entity.get('label', ''),
                    'type': entity.get('type', 'TEXT_INPUT'),
                    'options': entity.get('options', []),
                    'user_input': entity.get('user_input', '')
                }
                validated.append(clean_entity)

        return {
            "status": "Success",
            "validated_entities": validated,
            "total_entities": len(validated)
        }
    except Exception as e:
        logger.error(f"Error validating entities: {e}")
        raise HTTPException(status_code=500, detail="Error validating entities")


@app.post("/v1/chatbot-ai/reload-intents")
async def reload_intents(api_key: str = Depends(verify_api_key)):
    """Reload intents data from file."""
    try:
        from src.data.loader import data_loader
        # Clear cache to force reload
        data_loader._intents_cache = None
        intents_data = data_loader.load_intents_data()

        return {
            "status": "Success",
            "message": "Intents data reloaded",
            "intents_count": len(intents_data.get("intents", []))
        }
    except Exception as e:
        logger.error(f"Error reloading intents: {e}")
        raise HTTPException(status_code=500, detail="Error reloading intents")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")