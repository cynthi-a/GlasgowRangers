# VocaPoint
This is Team Glasgow Rangers' submission to HackZurich2017 which made it to the finale. 

## What is it and what does it do?
Our web application was build using Flask. The user can upload their PDF presentation and use the app to present it.
The app uses an offline speech-detection and classification library to listen for keywords that the user can associate with each slide. Whenever a keyword is detected, the web app jumps to the corresponding slide.
The application interprets audio streams in real-time using [PocketSpinx](https://github.com/cmusphinx/pocketsphinx) and works offline.

