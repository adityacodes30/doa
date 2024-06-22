# DOA : Speech-to-Text-to-Speech (STT-TTS) with AI Processing

This project combines speech recognition, AI-based text processing, and text-to-speech capabilities to create a pipeline for converting spoken input into processed speech output.

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Usage Instructions](#usage-instructions)
- [Assumptions](#assumptions)
- [Potential Issues](#potential-issues)
- [Notes](#notes)

## Setup and Installation

1. Clone the repository to your local machine.

2. Install the required dependencies with the command
   `pip install -r requirements.txt` .

3. Create a `.env` file in the project root directory with the following contents: `DG_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key`

Note: The project requires Python 3.10 or higher. For pyaudio, you may need to install the portaudio library. Instructions can be found [here](https://pypi.org/project/PyAudio/).

## Usage Instructions

1. Import the `DOA` class from `main.py`:

```python

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
```

# Speech Recognition and Text-to-Speech Project

## Assumptions

- The user has valid API keys for both DeepGram and OpenAI services.
- The system has a working microphone for speech input.
- The system has audio output capabilities for text-to-speech playback.
- The user has a stable internet connection for API calls.

## Potential Issues

1. **API Rate Limits**:
   - Both DeepGram and OpenAI have rate limits. Excessive usage may lead to temporary service interruptions.
2. **Microphone Access**:
   - The program may fail if it cannot access the system's microphone or if the microphone is not working properly.
3. **Audio Playback**:
   - Issues with the system's audio output could prevent the text-to-speech functionality from working correctly.
4. **Network Connectivity**:
   - Poor internet connection may cause delays or failures in API calls.
5. **Environment Variables**:
   - If the `.env` file is not set up correctly or API keys are invalid, the program will fail to authenticate with the services.
6. **Dependency Conflicts**:
   - Ensure all dependencies are installed and compatible with your Python version.
7. **Asynchronous Execution**:
   - Improper handling of asynchronous functions may lead to unexpected behavior or errors.
8. **Language Support**:
   - The current setup is optimized for English. Using other languages may require adjustments to the DeepGram and OpenAI API calls.
9. **Resource Usage**:
   - Continuous use of speech recognition and audio streaming may consume significant system resources and battery life on portable devices.
10. **Error Handling**:
    - While basic error handling is implemented, some edge cases may not be fully covered.

## Notes:
- Working on deploying this to PyPi and adding more features
- A more performant solution to stream chunk by chunk is still under developement and can be found in `utils/wip/ou2.py`
- The project is still in beta and may have some issues. Please report any bugs or suggestions for improvement.
- The project is for educational purposes only and should not be used in critical applications without proper testing and validation.

