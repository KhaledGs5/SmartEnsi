import speech_recognition
from googletrans import Translator
import pyttsx3
from tools import Tools

toul = Tools()
droid = pyttsx3.init()


class Chat:

    def __init__(self):

        self.language = "auto"
        self.name = "alexa"



    def reconise(self,delay):

        recognizer = speech_recognition.Recognizer()
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic, phrase_time_limit=delay)
                text = recognizer.recognize_google(audio, language= 'ar')

                if text is None:
                    return ""

                text = text.lower()
                text = self.translate(text)

                return (text)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()




    def translate(self,text):
        if (text):
            translator = Translator()
            translated_text = translator.translate(text,dest="en")
            translated_text = translated_text.text.lower()
            return translated_text




    def choose_language(self):

        droid.say("Choose your language please")
        droid.runAndWait()

        response = self.reconise(4)
        print(response)
        if(toul.find("arabic",response)):
            new_language = "ar-AR"
        elif(toul.find("frensh",response)):
            new_language = "fr-FR"
        else:
            new_language = "en-EN"

        self.language = new_language




    def start(self):
        name = "rrr"
        while (not toul.find(self.name,name)) :
            name = self.reconise(6)
            if(not name):
                name = "rrrr"
            print(f"wrong name{name}")
        print(f"correct name {name}")


