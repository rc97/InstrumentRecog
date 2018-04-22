import sys, time, math, array, wave
import numpy as np
import pyaudio as pa
from pydub import AudioSegment
from matplotlib import pyplot as plt
import fluidsynth

sys.path.insert(0, 'lib')
sys.path.insert(0, 'lib/x64')
import Leap

VOL_LOW = 0
VOL_HIGH = 600

BAS_LOW = -250
BAS_HIGH = 250

PIT_LOW = -250
PIT_HIGH = 250

MAX_VOL = 2**7-1
MAX_PIT = 880

FS = 96000

dt = .01

def posInRange(pos, low, high):
	val = (pos - low) / (high - low)
	return 0 if val < 0 else 1 if val > 1 else val

def main():

	fs = fluidsynth.Synth()
	fs.start()

	sfid = fs.sfload("grandPiano.sf2")
	fs.program_select(0, sfid, 0, 0)

	fs.noteon(0, 60, 30)
	fs.noteon(0, 67, 30)
	fs.noteon(0, 76, 30)

	time.sleep(1.0)

	fs.noteoff(0, 60)
	fs.noteoff(0, 67)
	fs.noteoff(0, 76)

	time.sleep(1.0)

	fs.delete()

	# vSound = AudioSegment.from_mp3("v1.mp3")
	# vRawData = vSound.raw_data
	# vSamples = np.fromstring(vRawData, dtype=np.int16)[5000:25000]

	# sd.default.samplerate = FS
	# controller = Leap.Controller()
	# p = pa.PyAudio()
	# stream = p.open(format=16,
	# 			channels=1,
 #                rate=FS,
 #                output=True)
	# t = 0
	# while(1):
	# 	frame = controller.frame()
	# 	pitch = 0
	# 	vol = 0
	# 	bass = 0
	# 	mix = 0

	# 	# Get hands
	# 	for hand in frame.hands:
	# 		if hand.is_right:
	# 			pos = hand.palm_position
	# 			x = pos[0]
	# 			y = pos[1]
	# 			z = pos[2]
	# 			pitch = MAX_PIT * posInRange(x, PIT_LOW, PIT_HIGH)
	# 			mix = posInRange(z, BAS_LOW, BAS_HIGH)
	# 			# print(x, y, z)
	# 			print("Pitch", pitch)
	# 			print("Mix", mix)
	# 		elif hand.is_left:
	# 			pos = hand.palm_position
	# 			x = pos[0]
	# 			y = pos[1]
	# 			z = pos[2]
	# 			vol = MAX_VOL * (posInRange(y, VOL_LOW, VOL_HIGH))
	# 			bass = posInRange(z, BAS_LOW, BAS_HIGH)
	# 			# print(x, y, z)
	# 			print("Volume", vol)
	# 			print("Bass", bass)
	# 			print()

	# 	if pitch > 0:
	# 		freq = pitch / FS * 3.14
	# 		ts = int(FS / pitch * 12)
	# 		pause = ts * 1.0 / FS
	# 		print(freq, ts, pause)
	# 		sine = [vol*math.sin(i * freq) for i in range(ts)]
	# 		sine2 = [vol*math.sin(2 * i * freq) for i in range(ts)]
	# 		bass = [vol*math.sin(i * freq / 2) for i in range(ts)]
	# 		sineBass = [i/2 + j/4 + k/4 for i, j, k in zip(sine, bass, sine2)]
	# 		square = [vol if i > 0 else -vol if i < 0 else 0 for i in sine]
	# 		mixSine = [mix * j + (1 - mix) * i for i, j in zip(sine, sine2)]
	# 		mixSquare = [mix/2 * j + (1 - mix/2) * i for i, j in zip(sine, square)]
	# 		samps = sineBass
	# 		samps = np.array(samps, dtype=np.int8)
	# 		sineStr = array.array('b', samps).tostring()
	# 		stream.write(sineStr)


if __name__ == '__main__':
	main()