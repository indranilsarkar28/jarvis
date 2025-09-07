import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import google.generativeai as genai   # ✅ Gemini

# Configure Gemini
genai.configure(api_key="AIzaSyABs3D46oI4d7rJBFXrtZC3i6EsQl1C79k")   # <-- paste your key here

def speak(text):
    print(f"Jarvis: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def get_news():
    api_key = "b9d20d36e92d4358ab53a44ad7f36997"   # your newsapi.org key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        headlines = [article["title"] for article in articles[:5]]
        return headlines if headlines else ["No news found."]
    except Exception as e:
        return [f"Error fetching news: {e}"]

def ask_ai(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # free + fast
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with AI: {e}"

def processCommand(c):
    print(f"Command received: {c}")
    if "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "news" in c.lower():
        speak("Here are the top headlines for today.")
        headlines = get_news()
        for h in headlines:
            speak(h)
    else:
        # ✅ Gemini fallback
        speak("Let me think...")
        reply = ask_ai(c)
        speak(reply)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            try:
                word = r.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    
                    while True:
                        try:
                            with sr.Microphone() as source:
                                print("Jarvis Active...")
                                r.adjust_for_ambient_noise(source, duration=0.5)
                                audio = r.listen(source)
                                command = r.recognize_google(audio)

                                if command.lower() in ["stop", "exit", "quit"]:
                                    speak("Okay, going back to sleep.")
                                    break
                                processCommand(command)

                        except sr.UnknownValueError:
                            print("Could not understand audio")
                            speak("Sorry, I didn't catch that. Please repeat.")
                            continue
                        except sr.RequestError as e:
                            print(f"Could not request results; {e}")
                            continue

            except sr.UnknownValueError:
                print("Could not understand wake word")
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                continue

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue
