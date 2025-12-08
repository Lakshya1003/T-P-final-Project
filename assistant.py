import os
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import pywhatkit
import subprocess
import threading
import time
from dotenv import load_dotenv
import database

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

class BlueberryAssistant:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.running = True
        
        # TTS Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        
        # Hotword Detection (Porcupine 1.9.5)
        self.keyword = "blueberry"
        try:
            # Check if blueberry is available or try to load it
            # Note: Porcupine 1.9.5 standard keywords usually don't include blueberry.
            # We try it, if it fails we fall back.
            self.porcupine = pvporcupine.create(keywords=[self.keyword])
            print(f"Hotword '{self.keyword}' initialized successfully.")
        except Exception as e:
            print(f"Could not initialize hotword '{self.keyword}': {e}")
            print("Falling back to 'porcupine'...")
            self.keyword = "porcupine"
            try:
                self.porcupine = pvporcupine.create(keywords=["porcupine"])
                print("Hotword 'porcupine' initialized successfully.")
            except Exception as e2:
                print(f"Error initializing fallback hotword: {e2}")
                self.porcupine = None

        self.pa = pyaudio.PyAudio()
        self.open_stream()

        # Speech Recognition
        self.recognizer = sr.Recognizer()

    def open_stream(self):
        """Open the PyAudio stream for Porcupine."""
        if self.porcupine:
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

    def close_stream(self):
        """Close the PyAudio stream to release microphone."""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

    def speak(self, text):
        """Speak text using pyttsx3."""
        if self.ui_callback:
            self.ui_callback("Blueberry", text)
        print(f"Blueberry: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def listen(self):
        """Listen for command after hotword."""
        # Ensure stream is closed before using SpeechRecognition
        self.close_stream()
        
        text = None
        with sr.Microphone() as source:
            print("Listening for command...")
            if self.ui_callback:
                self.ui_callback("System", "Listening...")
            
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"User said: {text}")
                if self.ui_callback:
                    self.ui_callback("User", text)
                text = text.lower()
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error listening: {e}")
        
        # Re-open stream for hotword detection
        self.open_stream()
        return text

    def process_command(self, command):
        """Process the recognized command."""
        if not command:
            return

        # 1. Custom Commands from DB
        db_cmd = database.get_command(command)
        if db_cmd:
            action_type, action_value = db_cmd
            if action_type == "open_url":
                import webbrowser
                webbrowser.open(action_value)
                self.speak(f"Opening {command}")
                return
            elif action_type == "speak":
                self.speak(action_value)
                return

        # 2. Built-in Commands
        if "open calculator" in command:
            self.speak("Opening Calculator")
            subprocess.Popen("calc.exe")
        
        elif "open vs code" in command or "open code" in command:
            self.speak("Opening Visual Studio Code")
            # Assuming VS Code is in path or default location
            try:
                subprocess.Popen("code")
            except:
                self.speak("I couldn't find VS Code.")

        elif "play" in command and "on youtube" in command:
            song = command.replace("play", "").replace("on youtube", "").strip()
            self.speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif "add command" in command:
            self.speak("What should be the command phrase?")
            phrase = self.listen()
            if phrase:
                self.speak(f"What should I say when you say {phrase}?")
                response = self.listen()
                if response:
                    database.add_command(phrase, "speak", response)
                    self.speak("Command added successfully.")

        # 3. Chatbot (Gemini)
        else:
            try:
                response = model.generate_content(command)
                reply = response.text
                # Keep it brief for TTS
                if len(reply) > 200:
                    short_reply = reply[:200] + "..."
                else:
                    short_reply = reply
                self.speak(short_reply)
            except Exception as e:
                print(f"Gemini Error: {e}")
                self.speak("I'm sorry, I couldn't process that.")

    def run(self):
        """Main loop."""
        if not self.porcupine:
            print("Porcupine not initialized. Exiting.")
import os
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import pywhatkit
import subprocess
import threading
import time
from dotenv import load_dotenv
import database

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

class BlueberryAssistant:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.running = True
        
        # TTS Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        
        # Hotword Detection (Porcupine 1.9.5)
        self.keyword = "blueberry"
        try:
            # Check if blueberry is available or try to load it
            # Note: Porcupine 1.9.5 standard keywords usually don't include blueberry.
            # We try it, if it fails we fall back.
            self.porcupine = pvporcupine.create(keywords=[self.keyword])
            print(f"Hotword '{self.keyword}' initialized successfully.")
        except Exception as e:
            print(f"Could not initialize hotword '{self.keyword}': {e}")
            print("Falling back to 'porcupine'...")
            self.keyword = "porcupine"
            try:
                self.porcupine = pvporcupine.create(keywords=["porcupine"])
                print("Hotword 'porcupine' initialized successfully.")
            except Exception as e2:
                print(f"Error initializing fallback hotword: {e2}")
                self.porcupine = None

        self.pa = pyaudio.PyAudio()
        self.open_stream()

        # Speech Recognition
        self.recognizer = sr.Recognizer()

    def open_stream(self):
        """Open the PyAudio stream for Porcupine."""
        if self.porcupine:
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

    def close_stream(self):
        """Close the PyAudio stream to release microphone."""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

    def speak(self, text):
        """Speak text using pyttsx3."""
        if self.ui_callback:
            self.ui_callback("Blueberry", text)
        print(f"Blueberry: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def listen(self):
        """Listen for command after hotword."""
        # Ensure stream is closed before using SpeechRecognition
        self.close_stream()
        
        text = None
        with sr.Microphone() as source:
            print("Listening for command...")
            if self.ui_callback:
                self.ui_callback("System", "Listening...")
            
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"User said: {text}")
                if self.ui_callback:
                    self.ui_callback("User", text)
                text = text.lower()
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error listening: {e}")
        
        # Re-open stream for hotword detection
        self.open_stream()
        return text

    def process_command(self, command):
        """Process the recognized command."""
        if not command:
            return

        # 1. Custom Commands from DB
        db_cmd = database.get_command(command)
        if db_cmd:
            action_type, action_value = db_cmd
            if action_type == "open_url":
                import webbrowser
                webbrowser.open(action_value)
                self.speak(f"Opening {command}")
                return
            elif action_type == "speak":
                self.speak(action_value)
                return

        # 2. Built-in Commands
        if "open calculator" in command:
            self.speak("Opening Calculator")
            subprocess.Popen("calc.exe")
        
        elif "open vs code" in command or "open code" in command:
            self.speak("Opening Visual Studio Code")
            # Assuming VS Code is in path or default location
            try:
                subprocess.Popen("code")
            except:
                self.speak("I couldn't find VS Code.")

        elif "play" in command and "on youtube" in command:
            song = command.replace("play", "").replace("on youtube", "").strip()
            self.speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif "add command" in command:
            self.speak("What should be the command phrase?")
            phrase = self.listen()
            if phrase:
                self.speak(f"What should I say when you say {phrase}?")
                response = self.listen()
                if response:
                    database.add_command(phrase, "speak", response)
                    self.speak("Command added successfully.")

        # 3. Chatbot (Gemini)
        else:
            try:
                response = model.generate_content(command)
                reply = response.text
                # Keep it brief for TTS
                if len(reply) > 200:
                    short_reply = reply[:200] + "..."
                else:
                    short_reply = reply
                self.speak(short_reply)
            except Exception as e:
                print(f"Gemini Error: {e}")
                self.speak("I'm sorry, I couldn't process that.")

    def run(self):
        """Main loop."""
        if not self.porcupine:
            print("Porcupine not initialized. Exiting.")
            return

        print(f"Blueberry Assistant Started. Waiting for hotword '{self.keyword}'...")
        if self.ui_callback:
            self.ui_callback("System", f"Blueberry is ready. Say '{self.keyword}' to wake me up.")

        self.manual_trigger = False

        while self.running:
            try:
                if self.audio_stream.is_active():
                    # Check for manual trigger
                    if self.manual_trigger:
                        print("Manual trigger detected!")
                        self.manual_trigger = False
                        self.speak("Yes?")
                        command = self.listen()
                        self.process_command(command)
                        continue

                    pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    
                    keyword_index = self.porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        print("Hotword Detected!")
                        self.speak("Yes?")
                        command = self.listen()
                        self.process_command(command)
                else:
                    # Stream might be closed or stopped, wait a bit
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Error in main loop: {e}")
                continue

    def trigger(self):
        """Manually trigger the assistant."""
        self.manual_trigger = True

    def stop(self):
        self.running = False
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
