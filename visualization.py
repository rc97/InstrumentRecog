import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
# import matplotlib.animation as animation

MAX_PIT = 880
VIS_HIST = 20
norm = matplotlib.colors.Normalize(vmin=0, vmax=MAX_PIT, clip=True)
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap='plasma')

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_ylim(0, 650)
plt.show(block=False)

ind = np.arange(1, 1+VIS_HIST)
pitchHist = np.zeros(VIS_HIST) # values from 0 to 880
volHist = np.zeros(VIS_HIST)
bars = plt.bar(ind, volHist)

print(volHist.shape)
print(len(bars))

def genPitch():
	return np.random.rand()*MAX_PIT

def genVol():
	return np.random.rand()*600

while (True):

	pitch = genPitch()
	vol = genVol()
	pitchHist[0:-1] = pitchHist[1:]
	pitchHist[-1] = pitch
	volHist[0:-1] = volHist[1:]
	volHist[-1] = vol
	for i in range(VIS_HIST):
		print(bars[i])
		print(volHist[i])
		bars[i].set_height(volHist[i])
		bars[i].set_facecolor(mapper.to_rgba(pitchHist[i]))

	# ask the canvas to re-draw itself the next time it
	# has a chance.
	# For most of the GUI backends this adds an event to the queue
	# of the GUI frameworks event loop.
	# fig.canvas.draw_idle()
	try:
		fig.canvas.flush_events()
	except NotImplementedError:
		pass
	time.sleep(0.02)