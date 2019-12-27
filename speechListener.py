
from watsontalker import sayWords
import time
# This module is imported so that we can  
# play the converted audio 
from playsound import playsound
#import os 

import speech_recognition as sr
import yaml
#try to read the config data from config.yaml
config = []
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Language in which you want to convert 
language = 'en'


def askName(confirmCorrect):
    name = []
    validResponse = False
    while (not validResponse):
        sayWords("Hey there!", config, True)
        time.sleep(.5)
        validName = False
        while (not validName):
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                
            
                validResponse = not confirmCorrect
                
                sayWords("What is your name?", config, True)

                # obtain audio from the microphone
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source) 
                    print("Say your name!")
                    audio = r.listen(source, phrase_time_limit=3, timeout = 5)

                name = r.recognize_google(audio)

                validName = True
                
            #if name != 'Unknown':
            #    cv2.imwrite(name + '.jpg', frame)
            except sr.WaitTimeoutError:
                    print("Waited too long to start phrase")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        noResponse = True
        while (noResponse):
            try:
                sayWords("Your name is", config, True)

                sayWords(name, config, True)
                sayWords("Is that right?",config, True)

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source) 
                    audio = r.listen(source, phrase_time_limit=3, timeout = 5)
                    response = r.recognize_google(audio)
                    if response == 'yes' or response == 'yeah' or response == 'that is right' or response == 'that is correct':
                        validResponse = True
                    print(response)
                    noResponse = False
            except sr.WaitTimeoutError:
                print("Waited too long to start phrase")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
    return name

#askName(True)