import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_duckduckgo(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url)
        data = response.json()
        answer = data.get("AbstractText")
        return answer if answer else "Sorry, I couldn't find an answer."
    except Exception as e:
        return f"DuckDuckGo error: {e}"

def processcommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open whatsapp" in c:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com/")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    
    elif c.lower().startswith("play"):
            song = c.lower().split(" ")[1]
            link = musiclibrary.music[song]
            webbrowser.open(link)
    elif "stop" in c.lower():
        speak("Good Bye")
        exit()
    else:
        speak("Let me think...")
        answer = ask_duckduckgo(c)
        print("GPT:", answer)
        speak(answer)

if __name__ == "__main__":
    speak("Initializing Jarvis.......")
    while True:
        try:
            print("Listening for wake word...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

            word = recognizer.recognize_google(audio)
            print("You said:", word)
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


    