import sounddevice as sd
from pydub import AudioSegment
import math
import numpy as np
import time

fs = 44100
pitch = 440

sd.default.samplerate = fs

audio = [1000*math.sin(i * pitch / fs * 3.14) + 100*math.sin(2 * i * pitch / fs * 3.14) for i in range(fs*1)]

vSound = AudioSegment.from_mp3("v1.mp3")

# # get raw audio data as a bytestring
# # check the following to make sure
# # but we are assuming 2 byte samples and 1 channel
# vRawData = vSound.raw_data

# vSamples = 5*np.fromstring(vRawData, dtype=np.int16)

# print(len(vSamples))

sd.play(audio, 44100)
time.sleep(.5)

audio = [1000*math.sin(2 * i * pitch / fs * 3.14) for i in range(fs*1)]
sd.play(audio)
time.sleep(1)