import time
import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    text =str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        #speak(query)
        time.sleep(1)
        eel.DisplayMessage(query) 
                

    except Exception as e:
        return ""
    
    return query.lower()



@eel.expose
def allCommands(message=1):
    
    if message==1:
        query = takeCommand()
        print(query)
    
    else:
        query=message
        
    try:
            
        if 'open' in query:
            from engine.action import openCommand
            openCommand(query)

        elif 'play' in query:
            from engine.action import PlayYoutube
            PlayYoutube(query)

        else:
            from engine.action import chatBot
            chatBot(query)
    except:
        print("Something Error Occured...")

    eel.ShowHood()

    