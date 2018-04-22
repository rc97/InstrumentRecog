import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation

MAX_PIT = 880
VIS_HIST = 10
norm = matplotlib.colors.Normalize(vmin=0, vmax=MAX_PIT, clip=True)
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap='plasma')

fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_ylim(0, 650)
plt.show(block=False)

ind = np.arange(1, 11)
pitchHist = np.zeros(VIS_HIST) # values from 0 to 880
volHist = np.zeros(VIS_HIST)
bars = plt.bar(ind, volHist)

print(volHist.shape)
print(len(bars))

def genPitch():
	return np.random.rand()*MAX_PIT

def genVol():
	return np.random.rand()*600

def animate(i):
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

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate,
                               frames=100, interval=100, blit=False)

plt.show()
