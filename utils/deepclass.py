from dotenv import load_dotenv
import os
from time import sleep
from colorama import Fore, Style
from yaspin import yaspin

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

class DeepGramUtil:
    def __init__(self):
        self.is_finals = []
        self.deepgram = DeepgramClient(os.getenv("DG_API_KEY"))
        self.dg_connection = self.deepgram.listen.live.v("1")
        self.microphone = Microphone(self.dg_connection.send)
        self.setup_event_handlers()
        self.is_running = False

    def setup_event_handlers(self):
        self.dg_connection.on(LiveTranscriptionEvents.Open, self.on_open)
        self.dg_connection.on(LiveTranscriptionEvents.Transcript, self.on_message)
        self.dg_connection.on(LiveTranscriptionEvents.Metadata, self.on_metadata)
        self.dg_connection.on(LiveTranscriptionEvents.SpeechStarted, self.on_speech_started)
        self.dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, self.on_utterance_end)
        self.dg_connection.on(LiveTranscriptionEvents.Close, self.on_close)
        self.dg_connection.on(LiveTranscriptionEvents.Error, self.on_error)
        self.dg_connection.on(LiveTranscriptionEvents.Unhandled, self.on_unhandled)

    def on_open(self, self2 , open, **kwargs):
        print(f"Connection Open")

    def on_message(self, self2 , result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        if result.is_final:
            self.is_finals.append(sentence)
            if result.speech_final:
                utterance = " ".join(self.is_finals)
                print(f"Speech Final: {utterance}")
                self.is_running = False
            else:
                print(f"Is Final: {sentence}")
        else:
            print(f"Interim Results: {sentence}")

    def on_metadata(self, self2 , metadata, **kwargs):
        print("")

    def on_speech_started(self, self2 , speech_started, **kwargs):
        print(f"Speech Started")

    def on_utterance_end(self, self2 , utterance_end, **kwargs):
        print(f"Utterance End")
        if len(self.is_finals) > 0:
            utterance = " ".join(self.is_finals)
            print(f"Utterance End: {utterance}")
            self.is_running = False
            

    def on_close(self, self2 , close, **kwargs):
        print(f"Connection Closed")

    def on_error(self, self2 , error, **kwargs):
        print(f"Handled Error: {error}")

    def on_unhandled(self, self2 , unhandled, **kwargs):
        print(f"Unhandled Websocket Message: {unhandled}")

    def start_transcription(self):
        try:
            options = LiveOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
                encoding="linear16",
                channels=1,
                sample_rate=16000,
                interim_results=True,
                utterance_end_ms="2000",
                vad_events=True,
                endpointing=300,
            )

            addons = {
                "no_delay": "true"
            }

            if self.dg_connection.start(options, addons=addons) is False:
                print("Failed to connect to Deepgram")
                return

            print( Fore.GREEN + "\n You can start speaking now\n")
            microphone = Microphone(self.dg_connection.send)

            microphone.start()
            spinner = yaspin(text="Listening...", color="green")
            spinner.start()

            self.is_running = True

            while self.is_running:
                sleep(0.001)

            microphone.finish()
            self.dg_connection.finish()
            
            print("Finished listening ✅")
            spinner.stop()

            return self.is_finals[0]

        except Exception as e:
            print(f"Could not open socket: {e}")