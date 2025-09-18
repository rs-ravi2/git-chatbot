import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "10000"))
    
    # Data file paths
    INTENTS_DATA_PATH: str = os.getenv("INTENTS_DATA_PATH", "src/data/intents.json")
    SAMPLE_RESPONSE_PATH: str = os.getenv("SAMPLE_RESPONSE_PATH", "src/data/sample_response_format.json")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
