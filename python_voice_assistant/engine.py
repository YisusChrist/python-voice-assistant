import sys

import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition


class Engine:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices, input = self._get_voices()
        self.voice = voices[input].id

    @property
    def voice(self):
        return self.engine.getProperty("voice")

    @voice.setter
    def voice(self, voice):
        self.engine.setProperty("voice", voice)

    def _get_voices(self):
        voices = self.engine.getProperty("voices")
        for i, v in enumerate(voices):
            print("Voice", i, v.id)

        choice = input("Select a voice: ")
        if not 0 <= int(choice) <= len(voices):
            print("Invalid input")
            return self.get_voices()

        return voices, int(choice)

    def speak(self, audio):
        if type(audio) != str:
            print("Enter a valid string")

        self.engine.say(audio)
        self.engine.runAndWait()

    def mic_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening ...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, phrase_time_limit=5)
            except KeyboardInterrupt:
                self.speak("Goodbye")
                sys.exit(1)
        try:
            print("Processing...")
            query = r.recognize_google(audio, language="en-in")
            print(query)
            return query
        except Exception as e:
            print(e)
            self.speak("Please repeat")
            return None
