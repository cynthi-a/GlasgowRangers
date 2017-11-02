from pocketsphinx import *
#!/usr/bin/env python
# module TEST_PYAUDIO

def get_keyword_from_audio():
    modeldir = get_model_path()

    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
    config.set_string(
        '-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
    config.set_string('-kws', 'keyphrase.list')

    p = pyaudio.PyAudio()
    #stream = p.open(format=pyaudio.paInt16, channels=1,
                    #rate=16000, input=True, frames_per_buffer=1024)
    stream = p.open(format=pyaudio.paInt16, channels=2,
                    rate=44100, input=True, frames_per_buffer=1024)
    stream.start_stream()

    decoder = Decoder(config)
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)
        if decoder.hyp() != None:
            this_key = decoder.hyp().hypstr
            decoder.end_utt()
            decoder.start_utt()
            return this_key

import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1.0
WAVE_OUTPUT_FILENAME = "file.wav"
TOTAL = int(RATE / CHUNK * RECORD_SECONDS)
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print "recording..."
frames = []

for i in range(0, TOTAL):
    print('reading {}/{}'.format(i,TOTAL))
    data = stream.read(CHUNK)
    frames.append(data)
print "finished recording"
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

get_keyword_from_audio()
