import sys, time, math, array, wave, threading, Queue
import matplotlib
import numpy as np
import pyaudio as pa
# from pydub import AudioSegment
from matplotlib import pyplot as plt

sys.path.insert(0, 'lib')
sys.path.insert(0, 'lib/x64')
import Leap

VOL_LOW = 50
VOL_HIGH = 500

BAS_LOW = -250
BAS_HIGH = 250

PIT_LOW = -100
PIT_HIGH = 250

MAX_VOL = 2**7-1
MAX_PIT = 1670

FS = 96000

dt = .01

q = Queue.Queue()

pitch = 0
vol = 0



def posInRange(pos, low, high):
	val = (pos - low) / (high - low)
	return 0 if val < 0 else 1 if val > 1 else val

class leapThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.controller = Leap.Controller()
		p = pa.PyAudio()
		self.stream = p.open(format=16,
				channels=1,
				rate=FS,
				output=True)
	def run(self):
		global pitch, vol
		while(1):
			frame = self.controller.frame()
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
				elif hand.is_left:
					pos = hand.palm_position
					x = pos[0]
					y = pos[1]
					z = pos[2]
					vol = 100 * (posInRange(y, VOL_LOW, VOL_HIGH))
					bass = posInRange(z, BAS_LOW, BAS_HIGH)

			if pitch > 0 and vol > 0:
				spec = [10, 25 * (rz - .5) if rz > .6 else 0, 50, 30 * (rz - .5) if rz > .6 else 0, 30 + (200*(.5-rz) if rz < .5 else 0)]
				sumSpec = sum(spec)
				spec = [i*1.0/sumSpec for i in spec]
				# print(spec)
				freq = pitch / FS * 3.14
				ts = int(FS / pitch * 12)
				# print(freq, ts)
				sine = [MAX_VOL * math.sin(i * freq) for i in range(ts)]
				sine2 = [MAX_VOL * math.sin(2 * i * freq) for i in range(ts)]
				bass = [MAX_VOL * math.sin(i * freq / 2) for i in range(ts)]
				chr1 = [MAX_VOL * math.sin(i * freq * 2**(-5.0/12)) for i in range(ts)]
				chr2 = [MAX_VOL * math.sin(i * freq * 2**(7.0/12)) for i in range(ts)]
				specMix = [i*spec[2] + j*spec[4] + k*spec[0] + l*spec[1] + m*spec[3] for i, j, k, l, m in zip(sine, sine2, bass, chr1, chr2)]
				samps = specMix
				samps = np.array(samps, dtype=np.int8)
				sineStr = array.array('b', samps).tostring()
				self.stream.write(sineStr)

			# print('QUEUE', pitch, vol)
			# q.put((pitch, vol))


def main():
	thread1 = leapThread(1, "Thread-1", 1)
	thread1.start()

	VIS_HIST = 20
	norm = matplotlib.colors.Normalize(vmin=0, vmax=MAX_PIT, clip=True)
	mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap='plasma')

	fig, ax = plt.subplots()
	ax.set_facecolor('black')
	ax.set_ylim(0, MAX_VOL+50)
	plt.show(block=False)

	ind = np.arange(1, 1+VIS_HIST)
	pitchHist = np.zeros(VIS_HIST)
	volHist = np.zeros(VIS_HIST)
	bars = plt.bar(ind, volHist)

	while(1):
		# while not q.empty():
		# 	(pitch, vol) = q.get(True)

		# print("PITCH", pitch, vol)
		pitchHist[0:-1] = pitchHist[1:]
		pitchHist[-1] = pitch
		volHist[0:-1] = volHist[1:]
		volHist[-1] = vol
		for i in range(VIS_HIST):
			# print(bars[i])
			# print(volHist[i])
			bars[i].set_height(volHist[i])
			bars[i].set_facecolor(mapper.to_rgba(pitchHist[i]))

		fig.canvas.draw_idle()
		try:
			fig.canvas.flush_events()
		except NotImplementedError:
			pass	
		time.sleep(.01)

	# time.sleep(10)
	thread1.join()

if __name__ == '__main__':
	main()