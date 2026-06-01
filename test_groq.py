import requests, os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('GROQ_API_KEY', 'NOT_FOUND')
print(f"Key found: {key[:10]}...")

r = requests.post(
    'https://api.groq.com/openai/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': 'hi'}],
        'max_tokens': 10
    },
    timeout=15
)
print('Status:', r.status_code)
print('Response:', r.json())