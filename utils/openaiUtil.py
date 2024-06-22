from dotenv import load_dotenv
load_dotenv()
import os
import httpx
import requests
import pyaudio
import soundfile as sf
import io
import time
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import pydub


class OpenAiUtil:
    def __init__(self , actionPrompt):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
        "Authorization": f"Bearer {self.api_key}"
        }
        self.actionPrompt : str = actionPrompt
        

    async def Action(self, user_message :str , max_tokens = 100):
        url = "https://api.openai.com/v1/engines/davinci/completions"
        data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": self.actionPrompt + user_message
            }
        ],
        "max_tokens": max_tokens
        }
        
        summary_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", json=data, headers=self.headers)
            response_data = response.json()
            

        return response_data['choices'][0]['message']['content'] , summary_time
    
    def stream_audio(self , input_text, model='tts-1', voice='alloy'):
        
        # OpenAI API endpoint and parameters
        print(f"sending for tts ")
        url = "https://api.openai.com/v1/audio/speech"
        

        data = {
            "model": model,
            "input": input_text,
            "voice": voice,
            "response_format": "opus",
        }

        audio = pyaudio.PyAudio()

        def get_pyaudio_format(subtype):
            if subtype == 'PCM_16':
                return pyaudio.paInt16
            return pyaudio.paInt16
        
        start_time = time.time()

        with requests.post(url, headers=self.headers, json=data, stream=True) as response:
            if response.status_code == 200:
                buffer = io.BytesIO()
                for chunk in response.iter_content(chunk_size=4096):
                    buffer.write(chunk)
            
                buffer.seek(0)

                with sf.SoundFile(buffer, 'r') as sound_file:
                    format = get_pyaudio_format(sound_file.subtype)
                    channels = sound_file.channels
                    rate = sound_file.samplerate
                    stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                    chunk_size = 1024
                    data = sound_file.read(chunk_size, dtype='int16')
                    print(f"Time to play: {time.time() - start_time} seconds")

                    while len(data) > 0:
                        stream.write(data.tobytes())
                        data = sound_file.read(chunk_size, dtype='int16')

                    stream.stop_stream()
                    stream.close()
            else:
                print(f"Error: {response.status_code} - {response.text}")

            audio.terminate()


            return start_time
    