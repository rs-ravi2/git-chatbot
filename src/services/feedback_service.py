import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.services.llm_service import llm_service
from src.utils.prompts import FEEDBACK_PROMPT

logger = logging.getLogger(__name__)


class FeedbackService:

    def __init__(self):
        pass

    async def analyze_feedback(self, feedback_message: str, target_language_code: str = "en") -> Dict[str, Any]:
        """
        Analyze sentiment, translate if needed, and extract keywords from feedback message
        """
        try:
            logger.info(f"Analyzing sentiment for feedback: {feedback_message[:50]}...")
            # Create the sentiment analysis prompt
            prompt = self._create_feedback_prompt(feedback_message, target_language_code)

            # Call LLM service
            llm_response = await llm_service.get_completion(
                prompt,
                "You are a helpful assistant that analyzes customer feedback sentiment and responds only in valid JSON format."
            )

            if "error" in llm_response:
                return self._create_error_response(llm_response["error"])

            # Process and validate the response
            return self._process_sentiment_response(llm_response)

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return self._create_error_response(str(e))

    def _create_feedback_prompt(self, feedback_message: str, target_language_code: str) -> str:
        """Create Feedback analysis prompt"""

        return FEEDBACK_PROMPT.format(feedback_message, target_language_code,target_language_code)

    def _process_sentiment_response(self, llm_response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate sentiment analysis response"""
        try:
            # Extract key information from LLM response
            sentiment = llm_response.get("sentiment", "neutral")
            translation = llm_response.get("translation", "")
            keywords = llm_response.get("keywords", [])

            # Validate sentiment value
            if sentiment not in ["positive", "negative", "neutral"]:
                logger.warning(f"Invalid sentiment value: {sentiment}, defaulting to neutral")
                sentiment = "neutral"

            # Ensure keywords is a list
            if not isinstance(keywords, list):
                logger.warning(f"Keywords is not a list: {keywords}, converting to empty list")
                keywords = []

            # Create success response
            return {
                "status": "Success",
                "result": [{
                    "sentiment": sentiment,
                    "translation": translation,
                    "keywords": keywords
                }]
            }

        except Exception as e:
            logger.error(f"Error processing sentiment response: {e}")
            return self._create_error_response(str(e))

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "status": "Error",
            "error": error_message,
            "result": [{
                "sentiment": "neutral",
                "translation": "",
                "keywords": []
            }]
        }


# Global instance
feedback_service = FeedbackService()