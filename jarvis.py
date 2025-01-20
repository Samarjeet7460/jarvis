import speech_recognition as sr
import datetime
import pyttsx3
import wikipedia
import pyjokes
import pywhatkit as kit
import pyautogui
import webbrowser
from AppOpener import open, close
import subprocess
import time
from googletrans import Translator
import google.generativeai as genai

API_KEY = "AIzaSyBnWc8zQQqtYwi-60Ubo_ZUuOJGwEaWZcI"

def initialize_tts_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    return engine

def say(engine, text):
    # print(text)
    engine.say(text)
    engine.runAndWait()

def wish_me(engine):
    hour = int(datetime.datetime.now().hour)
    greeting = "Good Morning Boss." if hour < 12 else "Good Afternoon Boss." if hour < 18 else "Good Evening Boss."
    say(engine, greeting)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error fetching results; {e}")
            return ""
    return ""

def translate_hindi_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='hi', dest='en')
        return translation.text.lower()
    except:
        return ""

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def open_application(query):
    app_name = query.replace("open ", "")
    open(app_name, match_closest=True)

def close_application(query):
    app_name = query.replace("close ", "").strip()
    close(app_name, match_closest=True, output=False)

def tell_time(engine):
    current_time = datetime.datetime.now().strftime("%H:%M")
    say(engine, f"The time is {current_time}")

def tell_joke(engine):
    joke = pyjokes.get_joke()
    say(engine, joke)

def search_amazon(query):
    message = query.replace("search on amazon ", "")
    url = 'https://www.amazon.in/s?k=' + message
    webbrowser.open(url)

def play_on_youtube(engine):
    say(engine, "What should I play on YouTube?")
    video_query = listen()
    kit.playonyt(video_query)

def switch_window():
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.keyUp("alt")

def search_google(query):
    kit.search(query)

def wikipedia_search(engine, query):
    try:
        query = query.replace("friday", "")
        summary = wikipedia.summary(query, sentences=2)
        say(engine, summary)
    except wikipedia.exceptions.DisambiguationError as e:
        say(engine, "There are multiple entries for this query. Please be more specific.")
    except wikipedia.exceptions.PageError:
        say(engine, "I can't find your query on Wikipedia.")

def process_query(engine, query):
    command_map = {
        "open youtube": open_youtube,
        "tell the time": lambda: tell_time(engine),
        "whats the time": lambda: tell_time(engine),
        "joke": lambda: tell_joke(engine),
        "switch tab": switch_window,
        "switch window": switch_window,
        "search on google": lambda: search_google(query),
    }

    for key in command_map:
        if key in query:
            command_map[key]()
            return True

    if "open" in query:
        open_application(query)
    elif "close" in query:
        close_application(query)
    elif "search on amazon" in query:
        search_amazon(query)
    elif "play on youtube" in query:
        play_on_youtube(engine)
    elif "according to wikipedia" in query:
        wikipedia_search(engine, query)
    elif 'sleep friday' in query or 'bye friday' in query:
        say(engine, "Bye boss")
        return False
    else:
        try:
            genai.configure(api_key="AIzaSyDqvkUKBkzVcHf8fJn_iJRLqFNiEwtneWc")
            model=genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="You are a AI desktop assistant. Your name is jarvis.")
            response = model.generate_content(
                query,
                generation_config = genai.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.1,
                    )
                )
            print(response.text)
            say(engine, response.text)
        except Exception as e:
            print(engine, f"Error: {e}")

    return True

if __name__ == '__main__':
    tts_engine = initialize_tts_engine()
    wish_me(tts_engine)

    while True:
        query = translate_hindi_to_english(listen())
        if not process_query(tts_engine, query):
            break
