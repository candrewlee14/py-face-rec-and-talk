import requests
from playsound import playsound
#import yaml
from slugify import slugify
#from msvcrt import getch
import os



def sayWords(text, config, playSound):
    slug = slugify(text+' '+config['voice'], max_length = 240)
    mp3s = os.listdir('voice_mp3s')

    if slug+'.mp3' in mp3s:
        slug = slug
    else:
        #prepare post request to IBM Watson Text-To-Speech API
        params = (
            ('accept', 'audio/mp3'),
            ('text', text),
            ('voice', config['voice']),
        )
        #send request
        response = requests.get(config['url'], params=params, auth=('apikey', config['apikey']))

        #save the response as a .mp3 sound file with the slug name
        open('voice_mp3s/'+slug+'.mp3', 'wb').write(response.content)

    #play the sound
    if playSound == True:
        playsound('voice_mp3s/'+slug+'.mp3')
    
    return

#this functions like a pause. The program waits for a key to finish. This allows the audio to play fully.
#junk = getch()

