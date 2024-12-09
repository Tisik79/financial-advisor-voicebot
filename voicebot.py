from fastapi import FastAPI, HTTPException
import anthropic
from tts import speak
import json
import os

app = FastAPI()
client = anthropic.Client(api_key=os.getenv('CLAUDE_API_KEY'))

def load_profile(profile_name):
    with open(f'profiles/{profile_name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_client_prompt(profile):
    return f"""Jsi klient finančního poradce s následujícími vlastnostmi:
    - Osobnost: {profile['osobnost']}
    - Finanční cíle: {profile['financni_cile']}
    - Tolerance rizika: {profile['tolerance_rizika']}
    - Situace: {profile['situace']}
    Odpovídej přirozeně na otázky poradce."""

@app.post('/start')
async def start_session(profile_name: str):
    profile = load_profile(profile_name)
    response = client.messages.create(
        model='claude-3-opus-20240229',
        max_tokens=1024,
        messages=[{
            'role': 'user',
            'content': get_client_prompt(profile)
        }]
    )
    speak(response.content)
    return {'response': response.content}

@app.post('/chat')
async def chat(message: str):
    response = client.messages.create(
        model='claude-3-opus-20240229',
        max_tokens=1024,
        messages=[{
            'role': 'user',
            'content': message
        }]
    )
    speak(response.content)
    return {'response': response.content}