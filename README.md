# Chatbot AI Service

A FastAPI-based chatbot service that uses OpenAI's API for intent classification and entity extraction.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env` file and update with your OpenAI API key
   - Update `src/data/intents.json` with your intent configurations

3. **Run the service:**
   ```bash
   # Development
   uvicorn src.main:app --reload

   # Production
   python -m src.main
   ```

## API Endpoints

- `POST /v1/chatbot-ai/process-message` - Process user messages
- `GET /health` - Health check
- `POST /v1/chatbot-ai/validate-entities` - Validate entity structure
- `POST /v1/chatbot-ai/reload-intents` - Reload intents from file

## Testing

```bash
curl -X POST "http://localhost:8000/v1/chatbot-ai/process-message" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to book an appointment for tomorrow morning"}'
```

## Project Structure

```
chatbot-ai/
├── src/
│   ├── config/          # Configuration management
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   ├── data/           # Data files and loaders
│   └── utils/          # Utility functions
├── tests/              # Test files
└── logs/              # Log files
```
