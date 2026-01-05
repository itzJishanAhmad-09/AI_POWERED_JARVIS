import os
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


from config import apikey 

openai.api_key = apikey


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  
engine.setProperty('rate', 175)  

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query
    except Exception as e:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return ""


def chat_with_gpt(prompt):
    messages = [
        {"role": "system", "content": "You are Jarvis, a helpful and witty AI assistant. Respond conversationally like a human."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        speak(reply)
    except Exception as e:
        speak("Sorry, I couldn't process that request.")
        print("Error:", e)


def handle_command(query):
    query = query.lower()

    if "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open wikipedia" in query:
        speak("Opening Wikipedia")
        webbrowser.open("https://www.wikipedia.org")
    elif "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in query:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")
    elif "exit" in query or "stop" in query or "quit" in query:
        speak("Goodbye, see you later.")
        exit()
    else:
        chat_with_gpt(query)


if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        query = take_command()
        if query:
            handle_command(query)
