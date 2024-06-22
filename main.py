from utils.deepclass import DeepGramUtil
from dotenv import load_dotenv
from utils.openaiUtil import OpenAiUtil
import asyncio
import time

class DOA:
    def __init__(self , actionPrompt):
        self.deepgram_util = DeepGramUtil()
        self.openai_util = OpenAiUtil(actionPrompt)

    async def start(self):
        transcript = self.deepgram_util.start_transcription()
        st = time.time()
        response , _  = await self.openai_util.Action(transcript)
        firstWordTime = self.openai_util.stream_audio(response)
        print(f"Time to transcription to first word uttered {firstWordTime - st}")


