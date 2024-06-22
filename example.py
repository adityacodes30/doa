from main import DOA
import asyncio

doa = DOA('summarise this text')

# speech to text 

def stt():
    result = doa.deepgram_util.start_transcription()
    print(result)

# get summary ( async fn )

async def summary():
    ip = "I was going to the beach where i encounteres sally shelling sea shells by the sea shore, I bought 2 shells for 2 dollars eacha nd got 2 crowns"
    result = await doa.openai_util.Action(ip)

# text to speech 

def tts():
    ip = "I was going to the beach where i encounteres sally shelling sea shells by the sea shore, I bought 2 shells for 2 dollars each and got 2 crowns"
    result = doa.openai_util.stream_audio(ip)
    print(result)

def main():
    ## cumulative fn that will run all 3 
    asyncio.run(doa.start())

if __name__ == "__main__":
    main()
