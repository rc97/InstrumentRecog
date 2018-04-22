import sys, time, math, array, wave
import numpy as np
import pyaudio as pa
from pydub import AudioSegment
from matplotlib import pyplot as plt

sys.path.insert(0, 'lib')
sys.path.insert(0, 'lib/x64')
import Leap

VOL_LOW = 0
VOL_HIGH = 600

BAS_LOW = -250
BAS_HIGH = 250

PIT_LOW = -100
PIT_HIGH = 250

MAX_VOL = 2**7-1
MAX_PIT = 1670

FS = 96000

dt = .01

def posInRange(pos, low, high):
	val = (pos - low) / (high - low)
	return 0 if val < 0 else 1 if val > 1 else val

def main():

	# vSound = AudioSegment.from_mp3("v1.mp3")
	# vRawData = vSound.raw_data
	# vSamples = np.fromstring(vRawData, dtype=np.int16)[5000:25000]

	# sd.default.samplerate = FS
	controller = Leap.Controller()
	p = pa.PyAudio()
	stream = p.open(format=16,
				channels=1,
                rate=FS,
                output=True)
	t = 0
	while(1):
		frame = controller.frame()
		pitch = 0
		vol = 0
		bass = 0
		mix = 0
		ry = 0
		rz = 0

		# Get hands
		for hand in frame.hands:
			if hand.is_right:
				pos = hand.palm_position
				x = pos[0]
				y = pos[1]
				z = pos[2]
				pitch = MAX_PIT * posInRange(x, PIT_LOW, PIT_HIGH)
				ry = posInRange(y, VOL_LOW, VOL_HIGH)
				mix = posInRange(z, BAS_LOW, BAS_HIGH)
				rz = posInRange(z, BAS_LOW, BAS_HIGH)
				# print(x, y, z)
				# print("Pitch", pitch)
				# print("Mix", mix)
			elif hand.is_left:
				pos = hand.palm_position
				x = pos[0]
				y = pos[1]
				z = pos[2]
				vol = MAX_VOL * (posInRange(y, VOL_LOW, VOL_HIGH))
				bass = posInRange(z, BAS_LOW, BAS_HIGH)
				# print(x, y, z)
				# print("Volume", vol)
				# print("Bass", bass)
				# print()

		if pitch > 0:
			spec = [15, 25 * (rz - .6) if rz > .6 else 0, 50 * ry - (20*(.5-rz) if rz < .5 else 0), 30 * (rz - .6) if rz > .6 else 0, 20 + (80*(.5-rz) if rz < .5 else 0)]
			sumSpec = sum(spec)
			spec = [i*1.0/sumSpec for i in spec]
			print(spec)
			freq = pitch / FS * 3.14
			ts = int(FS / pitch * 12)
			pause = ts * 1.0 / FS
			print(freq, ts, pause)
			sine = [vol*math.sin(i * freq) for i in range(ts)]
			sine2 = [vol*math.sin(2 * i * freq) for i in range(ts)]
			bass = [vol*math.sin(i * freq / 2) for i in range(ts)]
			chr1 = [vol*math.sin(i * freq * 2**(-5.0/12)) for i in range(ts)]
			chr2 = [vol*math.sin(i * freq * 2**(7.0/12)) for i in range(ts)]
			sineBass = [i/2 + j/4 + k/4 for i, j, k in zip(sine, bass, sine2)]
			square = [vol if i > 0 else -vol if i < 0 else 0 for i in sine]
			mixSine = [mix * j + (1 - mix) * i for i, j in zip(sine, sine2)]
			mixSquare = [mix/2 * j + (1 - mix/2) * i for i, j in zip(sine, square)]
			mixChr = [i*5/12 + j/6 + k/6 + l/6 + m/12 for i, j, k, l, m in zip(sine, sine2, bass, chr1, chr2)]
			specMix = [i*spec[2] + j*spec[4] + k*spec[0] + l*spec[1] + m*spec[3] for i, j, k, l, m in zip(sine, sine2, bass, chr1, chr2)]
			samps = specMix
			samps = np.array(samps, dtype=np.int8)
			sineStr = array.array('b', samps).tostring()
			stream.write(sineStr)


if __name__ == '__main__':
	main()