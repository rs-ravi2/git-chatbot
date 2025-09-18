CHATBOT_PROMPT = '''You are an expert intent and entity detection module service for a chatbot tasked with identification of information based on the customer messaged.
This will be used in a customer care chatbot.

Below is the intents and corresponding list of Entities per intent ( call it data-1) . Understand the meaning and context of information. 
Keep in mind to understand the meaning and context of intent and entities
{}

Task : Analyze the below user message and identify the matching intent and entity values found in the below user message:
User Input Message : {}

Use the below json structure and signature to provide the output:
{}

Methodology:
We have two types of entities, one of Text type and one of type with categorical options. Infer the understanding corresponding to the 
entity options and meaning based on the user message provided, and lets identify and provide the response in the provided response structure 

1. Identify the Matching intent and created a stub of the response signature using matching data 1
2. Set "user_input" key for "type"="text" entities and "response" "key" based on the matching possible options for "type"="options", based on the information present in user message. 
If the information is not there, set the parameter as null . But make sure to have all entities corresponding to the matched intent in data-1 in response

Go through the process, make sure to be correct and right about the identification of intent and entities and share the response finally a json format only
Final Output Format: Json
'''


FEEDBACK_PROMPT='''You are an expert sentiment analysis system for customer feedback. 

Task: Analyze the customer feedback message below and provide sentiment analysis, translation (if needed), and keyword extraction.

Customer Feedback Message: {}
Target Language Code: {}

Instructions:
1. Determine the sentiment of the feedback (positive, negative, or neutral)
2. If the feedback is not in the target language ({}), translate it to that language. If it's already in the target language, keep it as is.
3. Extract 3-5 relevant keywords that capture the essence of the feedback (focus on key issues, emotions, or topics mentioned)

Response Format (JSON only):
{{
    "sentiment": "positive|negative|neutral",
    "translation": "translated_or_original_message_here",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}

Guidelines:
- Sentiment should be "positive" for satisfied customers, "negative" for dissatisfied customers, "neutral" for mixed or factual feedback
- Translation should be natural and maintain the original meaning and tone
- Keywords should be lowercase, relevant terms that help categorize the feedback
- Focus on extracting keywords related to: service quality, agent behavior, product issues, emotions, specific problems mentioned

Provide only the JSON response with no additional text.'''
