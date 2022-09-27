###############################################################################
# Conway's Game of Life - Example 2
############################################################################### 

import numpy as np
from numpy import random
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Number of states
numStates = 12

# Size of game grid
gridSizeX = 64
gridSizeY = 64

# Convolution kernel, used for determining the number of neighbors
kernel = np.asarray([[1,1,1], [1,0,1], [1,1,1]])

# Random starting grid
mainGrid = random.randint(numStates, size=(gridSizeX, gridSizeY))

# Setup plot window
fig = plt.figure(frameon=False)
image = plt.imshow(mainGrid)
plt.axis('off')

def growth(neighborGrid):
    growthZone = (neighborGrid >= 20) & (neighborGrid <= 24)
    shrinkZone = (neighborGrid <= 18) | (neighborGrid >= 32)
    return 0 + growthZone - shrinkZone

# Function to update the grid
def update(frame):
    global mainGrid
    
    # Use 2D convolution to determine the number of active cells around each target cell
    neighborGrid = convolve2d(mainGrid, kernel, mode='same', boundary='wrap')
    
    # Determine whether cells grow, shrink or stay the same
    mainGrid = np.clip(mainGrid + growth(neighborGrid), 0, numStates - 1)
    
    # Update the plot image
    image.set_array(mainGrid)

# Run animation
anim = FuncAnimation(fig, update, interval=30, frames=500, repeat=False)

# Save as gif
writergif = PillowWriter(fps=30)
anim.save(r"C:\Users\zane4\Desktop\conway\example2\animation.gif", writer=writergif)

# Save kernel image
plt.imshow(kernel)
plt.savefig(r"C:\Users\zane4\Desktop\conway\example2\kernel.jpg")

# Save the growth function
plt.clf()
x = np.arange(0, 100, 1)
plt.plot(x, growth(x), color='black')
plt.axhspan(0, 1, facecolor='green', alpha=0.2)
plt.axhspan(-1, 0, facecolor='red', alpha=0.2)
plt.savefig(r"C:\Users\zane4\Desktop\conway\example2\growth.jpg")

