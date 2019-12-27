# py-face-rec-and-talk
Using the webcam to get video, the program looks for faces. If it sees a face it recognizes, it greets them. If not, it asks their name. Precursor to personal assistant-type software.\

## Setup
This program runs using several pip dependencies, so install those before running.
It also uses an IBM text-to-speech service. Create a file titled `config.yaml`, and paste this code: 
```
apikey: ***** (THIS IS THE KEY IBM GIVES YOU FOR ITS TEXT TO SPEECH SERVICE)
url: ****** (THIS IS THE LINK TO YOUR IBM SERVICE)
voice: en-GB_KateV3Voice (THERE ARE OTHER OPTIONS AVAILABLE, BUT HERE IS AN EXAMPLE VOICE
```
