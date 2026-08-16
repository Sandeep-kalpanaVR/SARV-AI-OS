import os
import sys
import json
import queue
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class SarvVoiceEngine:
    """
    Offline Voice & Speech Controller for SARV AI OS.
    Handles low-latency offline Text-To-Speech (TTS) and Vosk Speech-To-Text (STT).
    """
    def __init__(self, model_path: str = "models/vosk-model-small-en-us-0.15"):
        # 1. Initialize Offline TTS Engine
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty("voices")
            if voices:
                self.tts_engine.setProperty("voice", voices[0].id)
            self.tts_engine.setProperty("rate", 175)
        except Exception as e:
            print(f" [TTS INIT WARNING] {e}")
            self.tts_engine = None

        # 2. Initialize Vosk STT Model
        self.model_path = model_path
        self.audio_queue = queue.Queue()
        self.stt_model = None

        if os.path.exists(self.model_path):
            try:
                self.stt_model = Model(self.model_path)
                print(f" [VOICE ENGINE] Vosk model loaded from '{self.model_path}'")
            except Exception as e:
                print(f" [STT INIT ERROR] {e}")
        else:
            print(f" [VOICE ENGINE NOTICE] Vosk model not found at '{self.model_path}'. Text mode fallback active.")

    def speak(self, text: str):
        """Synthesizes text to speech offline."""
        if not text:
            return
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f" [TTS PLAYBACK ERROR] {e}")

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(bytes(indata))

    def listen_command(self, timeout_seconds: int = 8) -> str:
        """Listens through microphone and returns transcribed text using Vosk."""
        if not self.stt_model:
            print(" [STT NOTICE] Speech model not loaded. Please download the Vosk model.")
            return ""

        rec = KaldiRecognizer(self.stt_model, 16000)
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=self._audio_callback):
                print("\n🎤 Listening for voice command...")
                start_time = os.times().elapsed

                while os.times().elapsed - start_time < timeout_seconds:
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                        if rec.AcceptWaveform(data):
                            res = json.loads(rec.Result())
                            transcript = res.get("text", "").strip()
                            if transcript:
                                print(f" 🗣️ Recognized: '{transcript}'")
                                return transcript
                    except queue.Empty:
                        continue

                # Return any remaining audio in buffer
                final_res = json.loads(rec.FinalResult())
                transcript = final_res.get("text", "").strip()
                if transcript:
                    print(f" 🗣️ Recognized: '{transcript}'")
                    return transcript
        except Exception as e:
            print(f" [AUDIO RECORDING ERROR] {e}")

        return ""