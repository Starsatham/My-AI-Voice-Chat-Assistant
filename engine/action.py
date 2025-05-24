import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME,MY_KEY
import pywhatkit as kit
import winsound
import openai

def playAssistantSound():
    music_dir = os.path.abspath("www/assets/audio/start_sound.mp3")
    playsound(music_dir)
    winsound.PlaySound(music_dir, winsound.SND_FILENAME)

#click sound for mic button

@eel.expose
def playClickSound():
    music_dir = os.path.abspath("www/assets/audio/click_sound.mp3")
    playsound(music_dir)
    winsound.PlaySound(music_dir, winsound.SND_FILENAME)

conn = sqlite3.connect("star.db")
cursor = conn.cursor()

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query != "":
        try:
            # Try to find the application in sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return

            # If not found, try to find the URL in web_command table
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()
            
            if len(results) != 0:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            # If still not found, try to open using os.system
            speak("Opening " + query)
            try:
                os.system('start ' + query)
            except Exception as e:
                speak(f"Unable to open {query}. Error: {str(e)}")

        except Exception as e:
            speak(f"Something went wrong: {str(e)}")



def PlayYoutube(query):
    search_term = extract_yt_term(query)
    print(f"Extracted search term: {search_term}") 
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find what to play on YouTube.")

def extract_yt_term(command):
    # Adjusted regex to handle the phrase properly
    pattern = r'play\s+(.*)\s+(?:on\s+youtube)?$'  # Matches anything after 'play' (including 'on youtube')
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # Extract song name and remove extra spaces
    print(f"Failed to extract search term from command: {command}")  # Debugging line
    return None

#chatAI Bot

def chatBot(query):
    try:
        user_input = query.strip().lower()
       
        openai.api_key = MY_KEY; 
        # Call OpenAI's GPT-3.5 Turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "I am helpful AI assistant named STAR."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=200,
        )

        reply = response['choices'][0]['message']['content']
        # print("GPT Response:", reply)
        speak(reply)
        eel.DisplayMessage(reply)
        return reply

    except Exception as e:
        error_msg = "Sorry, the AI service is not responding right now."
        print(f"ChatBot Error: {e}")
        speak(error_msg)
        eel.DisplayMessage(error_msg)
