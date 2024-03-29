import random
import time
from enum import Enum

import pyttsx3

from text_to_speech_open_ai import TextToSpeechOpenAi

import gtts
import vlc


class ServiceType(Enum):
    PYTTSX3 = 'PYTTSX3'
    OPENAI = "OPENAI"
    GTTS = "gTTS",
    FUN_VOICE = "FUN_VOICE"


class TextToSpeechService:
    play = True

    def __init__(self, service=ServiceType.GTTS):
        self.service = service
        self.engine = self.__pyttsx3_tts_strategy(None, None)
        self._strategy_map = {
            ServiceType.GTTS: self.__google_tts_strategy,
            ServiceType.OPENAI: self.__openai_tts_strategy,
            ServiceType.PYTTSX3: self.__pyttsx3_tts_strategy,
            ServiceType.FUN_VOICE: self.__pyttsx3_fun_voice_tts_strategy,
        }

    def __pyttsx3_fun_voice_tts_strategy(self, text, path):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[random.choice([8, 10, 12, 48])].id)
        return engine

    def __pyttsx3_tts_strategy(self, text, path):
        engine = pyttsx3.init()

        engine.setProperty('rate', 150)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        return engine

    def __google_tts_strategy(self, text, path):
        tts = gtts.gTTS(text, lang="it")
        tts.save(path)

    def __openai_tts_strategy(self, text, path):
        text_to_speech_open_ai = TextToSpeechOpenAi()
        response = text_to_speech_open_ai.convert_to_speech(text)
        response.stream_to_file(path)

    def play_audio_from_text(self, text):

        if not TextToSpeechService.play: return

        path = "audio.mp3"

        # check if service is valid
        if self.service not in self._strategy_map:
            raise ValueError(
                f"Invalid service. Choose between {ServiceType.PYTTSX3.value} and {ServiceType.OPENAI.value}")

        # execute the associated function
        self._strategy_map[self.service](text, path)

        if self.service == ServiceType.PYTTSX3 or ServiceType.FUN_VOICE:
            self.engine.say(text)
            self.engine.runAndWait()

        else:
            # remaining code
            v = vlc.MediaPlayer(path)
            v.play()
            time.sleep(1)
            while v.is_playing():
                time.sleep(1)