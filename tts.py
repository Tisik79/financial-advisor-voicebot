import subprocess

def speak(text, language='cs'):
    try:
        subprocess.run(['espeak-ng', '-v', language, text])
    except Exception as e:
        print(f'TTS Error: {e}')
        return False
    return True