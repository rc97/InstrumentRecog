import sys, time, math, array, wave
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Process, Pipe

class ProcessPlotter(object):

	MAX_VOL = 2**7-1
	MAX_PIT = 1670
	VIS_HIST = 20

	def __init__(self):
		self.norm = matplotlib.colors.Normalize(vmin=0, vmax=self.MAX_PIT, clip=True)
		self.mapper = matplotlib.cm.ScalarMappable(norm=self.norm, cmap='plasma')
		self.fig, self.ax = plt.subplots()

		self.ax.set_facecolor('black')
		self.ax.set_ylim(0, self.MAX_VOL+50)
		plt.show(block=False)
		ind = np.arange(1, 1+self.VIS_HIST)
		self.pitchHist = np.zeros(self.VIS_HIST)
		self.volHist = np.zeros(self.VIS_HIST)
		self.bars = plt.bar(ind, self.volHist)

	def terminate(self):
		plt.close('all')

	def call_back(self):
		while self.pipe.poll():
			data = self.pipe.recv()
			if command is None:
				self.terminate()
				return False
			else:
				self.pitchHist[0:-1] = pitchHist[1:]
				self.pitchHist[-1] = data[0]
				self.volHist[0:-1] = volHist[1:]
				self.volHist[-1] = data[1]

			for i in range(VIS_HIST):
				print(self.bars[i])
				print(self.volHist[i])
				self.bars[i].set_height(volHist[i])
				self.bars[i].set_facecolor(mapper.to_rgba(pitchHist[i]))
			self.fig.canvas.draw_idle()
			try:
				self.fig.canvas.flush_events()
			except NotImplementedError:
				pass

	def __call__(self, pipe):
		print('Starting visualization')
		self.pipe = pipe
		timer = self.fig.canvas.new_timer(interval=10)
		timer.add_callback(self.call_back)
		timer.start()

		print('...done')
		plt.show()