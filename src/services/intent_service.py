import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.services.llm_service import llm_service
from src.data.loader import data_loader

logger = logging.getLogger(__name__)


class IntentService:

    def __init__(self):
        pass

    async def process_message(self, user_message: str, active_intent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user message using single unified prompt approach.
        Handles both intent classification and entity extraction in one call.
        The active_intent_id parameter is ignored since we use single prompt for everything.
        """
        try:
            # Get intents data (mapping)
            intents_data = data_loader.get_all_intents_formatted()

            # Get response format template
            response_format = data_loader.load_response_format()

            logger.info(f"Processing message with single prompt approach: {user_message}")
            if active_intent_id:
                logger.info(
                    f"Note: Active intent {active_intent_id} provided but single prompt approach will classify from scratch")

            # Call LLM with single unified prompt
            llm_response = await llm_service.process_message(
                intents_data, user_message, response_format
            )

            if "error" in llm_response:
                return self._create_error_response(llm_response["error"])

            response = llm_response
            if isinstance(llm_response,str):
                response = json.loads(llm_response)

            response["result"][0]["intent_changed"] = None
            response["result"][0]["previous_intentId"] = None
            # Process and validate the response
            return response

        except Exception as e:
            logger.error(f"Error in message processing: {e}")
            return self._create_error_response(str(e))

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "status": "Error",
            "error": error_message,
            "result": [{
                "intent": "Unknown",
                "is_matched": False,
                "intent_changed": None,
                "intentId": None,
                "previous_intentId": None,
                "entity": [],
                "metadata": {
                    "version": "v1.0",
                    "last_updated": datetime.now().isoformat(),
                    "source": "single-prompt-llm-service"
                }
            }]
        }


# Global instance
intent_service = IntentService()