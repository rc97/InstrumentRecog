import sys, time, math
import numpy as np
import sounddevice as sd
from pydub import AudioSegment

sys.path.insert(0, 'lib')
sys.path.insert(0, 'lib/x64')
import Leap

VOL_LOW = 0
VOL_HIGH = 600

BAS_LOW = -250
BAS_HIGH = 250

PIT_LOW = -250
PIT_HIGH = 250

MAX_VOL = 3
MAX_PIT = 880

FS = 44100

dt = .01

def posInRange(pos, low, high):
	val = (pos - low) / (high - low)
	return 0 if val < 0 else 1 if val > 1 else val

def main():

	# vSound = AudioSegment.from_mp3("v1.mp3")
	# vRawData = vSound.raw_data
	# vSamples = np.fromstring(vRawData, dtype=np.int16)[5000:25000]

	sd.default.samplerate = FS
	controller = Leap.Controller()
	t = 0
	while(1):
		frame = controller.frame()
		pitch = 0
		vol = 0
		bass = 0
		typ = 0

		# Get hands
		for hand in frame.hands:
			if hand.is_right:
				pos = hand.palm_position
				x = pos[0]
				y = pos[1]
				z = pos[2]
				pitch = MAX_PIT * posInRange(x, PIT_LOW, PIT_HIGH)
				typ = posInRange(z, BAS_LOW, BAS_HIGH)
				# print(x, y, z)
				print("Pitch", pitch)
				print("Type", typ)
			elif hand.is_left:
				pos = hand.palm_position
				x = pos[0]
				y = pos[1]
				z = pos[2]
				vol = MAX_VOL * (posInRange(y, VOL_LOW, VOL_HIGH))*3
				bass = posInRange(z, BAS_LOW, BAS_HIGH)
				# print(x, y, z)
				print("Volume", vol)
				print("Bass", bass)
				print()

		sine = [vol*math.sin((i + t*FS) * pitch / FS * 3.14) for i in range(FS)]
		sine2 = [vol*math.sin(2 * ((i + t*FS) * pitch / FS * 3.14)) for i in range(FS)]
		mix = [typ * j + (1 - typ) * i for i, j in zip(sine, sine2)]
		square = [vol*1.0 if i > 0 else -vol*1.0 if i < 0 else 0.0 for i in sine]
		if typ > .9:
			sd.play(sine2)
		elif typ < .1:
			sd.play(sine)
		else:
			sd.play(mix)
		time.sleep(dt)
		t += dt
		if t >= 1:
			t -= 1

if __name__ == '__main__':
	main()