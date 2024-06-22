from dotenv import load_dotenv
load_dotenv()
import os
import httpx
import asyncio
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
import queue
import threading
buffer = queue.Queue()

class OpenAiUtil:
    def __init__(self , actionPrompt):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
        "Authorization": f"Bearer {self.api_key}"
        }
        self.actionPrompt : str = actionPrompt
        self.ext = False

        

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
        
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", json=data, headers=self.headers)
            response_data = response.json()

        return response_data
    
    def streamed_audio(self , input_text, model='tts-1', voice='alloy'):
        start_time = time.time()
        # OpenAI API endpoint and parameters
        print(f"running")
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
        
        self.ext = False
        lock = threading.Lock()

        with requests.post(url, headers=self.headers, json=data, stream=True) as response:
            if response.status_code == 200:

                def reqest_handler():
                    for chunk in response.iter_content(chunk_size=4096):
                        buffer.put(chunk)
                        lock.acquire()
                        self.ext = True
                        lock.release()
                        while self.ext:
                            continue
                    buffer.put(None)
                    
                def player():
                    time.sleep(0.11)
                    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
                    
                    try:
                        while True :
                            while not self.ext:
                                continue
                            try:
                                data = buffer.get_nowait()
                            except queue.Empty:
                                print("Buffer is empty")
                                time.sleep(0.01)  
                                continue
                            stream.write(data)
                            lock.acquire()
                            self.ext = False
                            lock.release()
                    except queue.Empty:
                        print("Buffer is empty, waiting for data...")
                    finally:
                        stream.stop_stream()
                        stream.close()
                

                
                request_thread = threading.Thread(target=reqest_handler)
                player_thread = threading.Thread(target=player)

                request_thread.start()
                player_thread.start()

                request_thread.join()
                player_thread.join()

                audio.terminate()
                print("Playback completed")

            else:
                print(f"Error: {response.status_code} - {response.text}")

            audio.terminate()

            return f"Time to play: {time.time() - start_time} seconds"
    
async def main():
    openai_util = OpenAiUtil("summarise this text in first person")
    response = await openai_util.Action("i want to go to the hillsa nd have some ofeer with tea and then i want to help the needy people in the world . Then i want to go to the moon and have some fun with the aliens." , 20)
    print(response['choices'][0]['message']['content'])
    openai_util.streamed_audio(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']
        


asyncio.run(main())


