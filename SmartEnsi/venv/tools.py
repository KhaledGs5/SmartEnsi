import pygame
import pyttsx3
import pyaudio
from googletrans import Translator

eng = pyttsx3.init()

eng.setProperty('rate', 150)
eng.setProperty('volume', 0.9)


class Tools():

    def __init__(self):
        self.isSpeaking = False

    def find(self, mot, chaine):
        mots_chaine = chaine.split()  # Divise la chaîne en une liste de mots
        if mot in mots_chaine:
            return True
        else:
            return False

    def speak(self, string):
        voices = eng.getProperty('voices')

        # Select a French voice
        french_voice_id = None
        for voice in voices:
            if "english" in voice.name.lower():
                french_voice_id = voice.id
                break

        eng.setProperty('voice', french_voice_id)

        self.isSpeaking = True
        eng.say(string)
        eng.runAndWait()
        self.isSpeaking = False

    def speak_french(self, string):
        voices = eng.getProperty('voices')

        # Select a French voice
        french_voice_id = None
        for voice in voices:
            if "french" in voice.name.lower():
                french_voice_id = voice.id
                break

        eng.setProperty('voice', french_voice_id)

        self.isSpeaking = True
        eng.say(string)
        eng.runAndWait()
        self.isSpeaking = False

    def translate(self, text):
        translator = Translator()
        translated_text = translator.translate(text)
        translated_text = translated_text.text.lower()
        return translated_text

    def translate_french(self, text):
        translator = Translator()
        translated_text = translator.translate(text, dest='fr')
        translated_text = translated_text.text.lower()
        return translated_text

    def sound_play(self, mp3_file):
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
