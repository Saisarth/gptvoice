import openai
import os
import speech_recognition as sr  # Converts voice commands to text
import pyttsx3  # Reads text output to voice
import webbrowser

# Load API Key securely (Set the environment variable OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI Model Configuration
MODEL = "gpt-3.5-turbo"

def reply(question):
    """Get a response from OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "I'm having trouble processing that request."

# Text-to-Speech Configuration
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to the user and recognize speech."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in").lower()
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please repeat.")
            return None
        except sr.RequestError:
            print("Speech service is unavailable.")
            return None

def open_website(command):
    """Open a website based on the command."""
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "wikipedia": "https://www.wikipedia.org",
    }
    
    for site in sites:
        if site in command:
            webbrowser.open(sites[site])
            speak(f"Opening {site}")
            return True
    return False

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    while True:
        query = take_command()
        if query is None:
            continue

        if "bye" in query:
            speak("Goodbye! Have a great day!")
            break

        # Check if user wants to open a website
        if open_website(query):
            continue
        
        # Otherwise, answer the question using OpenAI
        ans = reply(query)
        print(ans)
        speak(ans)
