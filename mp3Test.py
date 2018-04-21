import libsoundtouch as lst
from pydub import AudioSegment
import numpy as np
from numpy import fft
from matplotlib import pyplot as plt

N_FFT = 2**17

vSound = AudioSegment.from_mp3("v1.mp3")

# get raw audio data as a bytestring
# check the following to make sure
# but we are assuming 2 byte samples and 1 channel
vRawData = vSound.raw_data

vSamples = np.fromstring(vRawData, dtype=np.int16)
print('time', len(vSamples))
plt.subplot(321)
plt.plot(vSamples)
# plt.show()

vfft = fft.rfft(vSamples, n=N_FFT)[:8192]
print('frequency', len(vfft))
plt.subplot(322)
plt.plot(np.absolute(vfft))
# plt.show()

fSound = AudioSegment.from_mp3("f1.mp3")

# get raw audio data as a bytestring
# check the following to make sure
# but we are assuming 2 byte samples and 1 channel
fRawData = fSound.raw_data

fSamples = np.fromstring(fRawData, dtype=np.int16)
print('time', len(fSamples))
plt.subplot(323)
plt.plot(fSamples)
# plt.show()

ffft = fft.rfft(fSamples, n=N_FFT)[:8192]
print('frequency', len(ffft))
plt.subplot(324)
plt.plot(np.absolute(ffft))
# plt.show()

tSound = AudioSegment.from_mp3("t1.mp3")

# get raw audio data as a bytestring
# check the following to make sure
# but we are assuming 2 byte samples and 1 channel
tRawData = tSound.raw_data

tSamples = np.fromstring(tRawData, dtype=np.int16)
print('time', len(tSamples))
plt.subplot(325)
plt.plot(tSamples)
# plt.show()

tfft = fft.rfft(tSamples, n=N_FFT)[:8192]
print('frequency', len(tfft))
plt.subplot(326)
plt.plot(np.absolute(tfft))
plt.show()