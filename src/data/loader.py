import json
import os
import logging
from typing import Dict, Any, Optional, List
from src.config.settings import settings

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        self._intents_cache = None

    def load_intents_data(self) -> Dict[str, Any]:
        """Load intents configuration from JSON file"""
        if self._intents_cache is not None:
            return self._intents_cache

        try:
            if not os.path.exists(settings.INTENTS_DATA_PATH):
                logger.warning(f"Intents file not found at {settings.INTENTS_DATA_PATH}")
                return {}

            with open(settings.INTENTS_DATA_PATH, 'r', encoding='utf-8') as file:
                self._intents_cache = json.load(file)
                logger.info(f"Loaded intents data from {settings.INTENTS_DATA_PATH}")
                return self._intents_cache

        except Exception as e:
            logger.error(f"Error loading intents data: {e}")
            return {}

    def get_intent_config(self, intent_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific intent"""
        intents_data = self.load_intents_data()

        # Search through intents structure - adjust based on your JSON structure
        if 'intents' in intents_data:
            for intent in intents_data['intents']:
                if intent.get('id') == intent_id:
                    return intent

        # Alternative structure - direct intent mapping
        return intents_data.get(intent_id)

    def get_all_intents_formatted(self) -> str:
        """Get formatted string representation of all intents for prompts"""
        intents_data = self.load_intents_data()

        try:
            # Format the intents data for the prompt
            return json.dumps(intents_data, indent=2)
        except Exception as e:
            logger.error(f"Error formatting intents data: {e}")
            return "{}"

    def load_response_format(self) -> str:
        """Load sample response format from JSON file"""
        try:
            response_format_path = settings.SAMPLE_RESPONSE_PATH
            if not os.path.exists(response_format_path):
                logger.warning(f"Response format file not found at {response_format_path}")
                # Return default format
                default_format = {
                    "intent": "intent_name_or_Unknown",
                    "is_matched": True,
                    "intentId": "intent_id_or_null",
                    "entity": [
                        {
                            "id": "entity_id",
                            "label": "Entity Label",
                            "type": "TEXT_INPUT",
                            "options": [],
                            "user_input": "extracted_value_or_null",
                            "response": "matched_option_or_null"
                        }
                    ]
                }
                return json.dumps(default_format, indent=2)

            with open(response_format_path, 'r', encoding='utf-8') as file:
                response_format = json.load(file)
                return json.dumps(response_format, indent=2)

        except Exception as e:
            logger.error(f"Error loading response format: {e}")
            # Return minimal format on error
            return '{"intent": "Unknown", "is_matched": false, "intentId": null, "entity": []}'

    def get_entities_for_intent(self, intent_id: str) -> List[Dict[str, Any]]:
        """Get entities list for specific intent"""
        intent_config = self.get_intent_config(intent_id)
        if intent_config:
            return intent_config.get('entity', [])
        return []


# Global instance
data_loader = DataLoader()