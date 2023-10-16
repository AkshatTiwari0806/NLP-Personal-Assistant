# for speech-to-text
import speech_recognition as sr

# for text-to-speech
from gtts import gTTS

# for language model
import transformers

import os
import time

# for data
import os
import datetime
import numpy as np

# Building the AI
class ChatBot():
    def __init__(self, name):
        print("----- Starting up", name, "-----")
        self.name = name

    def get_input(self):
        choice = input("Enter 'T' for text input or 'S' for speech input: ").lower()
        if choice == 't':
            self.text_input()
        elif choice == 's':
            self.speech_input()
        else:
            print("Invalid input. Please enter 'T' or 'S' for text or speech input.")
            self.get_input()

    def text_input(self):
        self.text = input("You: ")

    def speech_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            self.text = "ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("Me  --> ", self.text)
        except:
            print("Me  -->  ERROR")

    @staticmethod
    def text_to_speech(text):
        print("Dev --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)

        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system('start res.mp3')  # if you are using Mac->afplay or else for Windows->start
        time.sleep(int(50*duration))
        os.remove("res.mp3")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

# Running the AI
def main():
    ai = ChatBot(name="dev")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    ex = True
    while ex:
        ai.get_input()  # Prompt the user for input

        ## wake up
        if ai.wake_up(ai.text) is True:
            res = "Hello, I am Dave the AI, what can I do for you?"

        ## action time
        elif "time" in ai.text:
            res = ai.action_time()

        ## respond politely
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(["you're welcome!", "anytime!", "no problem!", "cool!", "I'm here if you need me!", "mention not"])

        elif any(i in ai.text for i in ["exit", "close"]):
            res = np.random.choice(["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "peace out!"])
            ex = False

        ## conversation
        else:
            if ai.text == "ERROR":
                res = "Sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()

        ai.text_to_speech(res)
        # Wait for the TTS operation to complete before moving to the next iteration
        while True:
            if os.path.exists("res.mp3"):
                time.sleep(1)
            else:
                break

    print("----- Closing down Dev -----")

if __name__ == "__main__":
    main()