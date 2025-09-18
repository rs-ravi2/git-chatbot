import json
import logging
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from src.config.settings import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

    async def get_completion(self, prompt: str, system_message: str = None) -> Dict[str, Any]:
        """Get completion from OpenAI API using LangChain"""
        try:
            messages = []

            if system_message:
                messages.append(SystemMessage(content=system_message))

            messages.append(HumanMessage(content=prompt))

            # Use ainvoke for async call
            response = await self.llm.ainvoke(messages)
            content = response.content

            logger.info(f"LLM Response: {content}")

            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Raw response: {content}")
                return {"error": "Invalid JSON response from LLM"}

        except Exception as e:
            logger.error(f"Error getting LLM completion: {e}")
            return {"error": str(e)}

    async def process_message(
            self,
            intents_data: str,
            user_message: str,
            response_format: str
    ) -> Dict[str, Any]:
        """Process user message using single unified prompt"""
        try:
            from src.utils.prompts import CHATBOT_PROMPT

            prompt = CHATBOT_PROMPT.format(
                intents_data,
                user_message,
                response_format
            )

            system_message = "You are a helpful assistant that responds only in valid JSON format."

            return await self.get_completion(prompt, system_message)

        except Exception as e:
            logger.error(f"Error in single prompt processing: {e}")
            return {"error": str(e)}


# Global instance
llm_service = LLMService()