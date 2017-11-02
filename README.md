# VocaPoint
This is Team Glasgow Rangers' submission to HackZurich2017 which made it to the finale. 

## What is it and what does it do?
Our web application was build using Flask. The user can upload their PDF presentation and use the app to present it.
The app uses an offline speech-detection and classification library to listen for keywords that the user can associate with each slide. Whenever a keyword is detected, the web app jumps to the corresponding slide.
The application interprets audio streams in real-time using [PocketSpinx](https://github.com/cmusphinx/pocketsphinx) and works offline.

## Set it up
You need to install a few libraries to get the website running on your computer. We assume that you have a working python (version 2) environment, including some command line tool and a package manager. The libraries required and some useful commands can be found in the file website/setup.txt. 

## Run it
To see the website locally, run 

```sh
$ python2 websiste/run.py
```

from this folder, and open a webbrowser at the local link, shown in the response of the above command.
