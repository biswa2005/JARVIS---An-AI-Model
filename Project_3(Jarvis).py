import speech_recognition as sr
import requests
import pyttsx3
import pyjokes
import datetime
import wikipedia
import webbrowser
from ytmusicapi import YTMusic
import yt_dlp
import vlc
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
ytmusic = YTMusic()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def websearch(url):
    webbrowser.open(url)


def play_music(query):
    """Search for a song on YouTube Music and stream it directly."""
    print(f"Searching for '{query}' on YouTube Music...")
    search_results = ytmusic.search(query, filter='songs')
    
    if not search_results:
        print("No results found.")
        return

    song_info = search_results[0]
    song_title = song_info['title']
    video_id = song_info['videoId']
    print(f"Playing: {song_title}")
    

    url = f"https://www.youtube.com/watch?v={video_id}"
    
 
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        play_url = info['url']
    
    player = vlc.MediaPlayer(play_url)
    player.play()

    duration = info['duration']
    print(f"Duration: {duration // 60}:{duration % 60} minutes")
    time.sleep(duration)
    player.stop()


def news():

    api_key = "678c8ce1f8e948098c6c23ed82e96f60"
    url = "https://newsapi.org/v2/top-headlines"

# Define parameters
    params = {
    "country": "us",  # Fetch news from a specific country, e.g., "us" for the United States
    "category": "technology",  # Optional: category like technology, business, sports
    "apiKey": api_key
}

# Make the request
    response = requests.get(url, params=params)

# Check if the request was successful
    if response.status_code == 200:
    # Parse JSON response
        data = response.json()
        articles = data.get("articles", [])

    # Display each article's title and description
    
    count = 5
    retrieved_articles = 0
    speak("for more details about news click on the url link")
    for article in articles:
        heading = article.get("title")
        title = heading.split(" -")[0] 
        if '[Removed]' in title:
            continue
        print(title)
        print("\n",article.get("description"))
        speak(title)
        speak(article.get("description"))
        print("\n\n URL :- ", article.get("url"))
        print("\n")
        retrieved_articles += 1

        if retrieved_articles == count:
            break


def weather(city):
    # Set up the API key and endpoint
    api_key = "d64501260fa18aef8771d0550f9218e5"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# Make the request
    response = requests.get(url)
# Check if the request was successful
    if response.status_code == 200:
    # Parse JSON response
        data = response.json()
    
    # Extract relevant information
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
    
        speak(f"Weather in {city}:")
        speak(f"Temperature: {temperature}°C")
        speak(f"Description: {weather_description}")
        speak(f"Humidity: {humidity}%")
        speak(f"Wind Speed: {wind_speed} m/s")
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {weather_description}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        speak("Failed to retrieve weather data. Check your city name.")


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning, Sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon, Sir!")
    elif 18 <= hour < 23:
        speak("Good evening, Sir!")
    else:
        speak("Good night, Sir!")
    speak("How can i help you sir")


def commandintake():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again, please...")
        return None


def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p") 
    speak(f"The current time is {current_time}")
    print(f"The current time is {current_time}")


def tell_joke():
    if "tell me a joke" in command:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
    else:
        for joke in pyjokes.get_jokes():
            print(joke)
            speak(joke)





if _name_ == "_main_":
    speak("Initializing Jarvis...")
    
    while True:
        command = commandintake()
        if command and command.startswith("hello jarvis"):
                 command = command.replace("hello jarvis", "").strip()
                 wishme()

        if command:

            if 'stop' in command or 'bye' in command or 'exit' in command:
                speak("Cooling down jarvis...")
                break

            elif 'how are you' in command or 'how r u' in command :
                speak("Im fine how about you!!")
            
            elif 'time' in command :
                tell_time()

            elif 'what is' in command:
                speak("Searching in Wikipedia...")
                command = command.replace("wikipedia", "")
                try:
                    result = wikipedia.summary(command, sentences=2)
                    speak("According to Wikipedia...")
                    print(result)
                    speak(result)
                except Exception as e:
                    speak("Sorry, I couldn't find any information on that topic.")

            elif 'search' in command:
                parts = command.split("search",1)
                query = parts[1].strip()
                url = f"https://www.google.com/search?q={query}"
                websearch(url)
            

            elif 'tell me a joke' in command or 'tell me some jokes' in command:
                tell_joke()
            
            
            
            elif 'play' in command:
                parts = command.split("play", 1)
                query = parts[1].strip()
                play_music(query)

            elif 'news' in command:
                news()

            elif 'weather' in command:
                speak("Please tell the city name : ")
                city = commandintake()
                weather(city)

            else:
                speak("Didn't understand, can you please say it again, sir?")