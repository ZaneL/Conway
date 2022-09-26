# Conway's Game of Life - Example 1

![Example 1](https://i.ibb.co/mNFnCMg/example1.gif)

```python
###############################################################################
# Conway's Game of Life - Example 1
############################################################################### 

import numpy as np
from numpy import random
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Size of game grid
gridSizeX = 64
gridSizeY = 64

# Convolution kernel, used for determining the number of neighbors
kernel = np.asarray([[1,1,1], [1,0,1], [1,1,1]])

# Random starting grid
mainGrid = random.randint(2, size=(gridSizeX, gridSizeY))

# Setup plot window
fig = plt.figure(frameon=False)
image = plt.imshow(mainGrid)
plt.axis('off')

# Function to update the grid
def update(frame):
    global mainGrid
    
    # Use 2D convolution to determine the number of active cells around each target cell
    neighborGrid = convolve2d(mainGrid, kernel, mode='same', boundary='wrap')
    
    # After an update, a given cell is alive if and only if one of these two conditions is true:
    # 1. It was already alive and had 2 or 3 neighbours.
    # 2. It was dead and had exactly 3 neighbours.
    #
    # This can be written in a boolean format as:
    # isAlive = (isAlive AND (neighbors = 3 OR neighbors = 2)) OR (NOT(isAlive) AND neighbors = 3)
    # Which can be simplified to:
    # isAlive =  (isAlive AND neighbors = 2) OR (neighbors = 3)
    mainGrid = (mainGrid & (neighborGrid==2)) | (neighborGrid==3)
    
    # Update the plot image
    image.set_array(mainGrid)

# Run animation
anim = FuncAnimation(fig, update, interval=30, frames=120, repeat=False)

# Save as gif
writergif = PillowWriter(fps=10)
anim.save(r"C:\Users\zane4\Desktop\conway\example1.gif", writer=writergif)
```

# Conway's Game of Life - Example 2

![Example 2](https://i.ibb.co/G30xMVz/example2.gif)

```python
###############################################################################
# Conway's Game of Life - Example 2
############################################################################### 

import numpy as np
from numpy import random
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

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
anim = FuncAnimation(fig, update, interval=30, frames=1000, repeat=False)

# Save as gif
writergif = PillowWriter(fps=25)
anim.save(r"C:\Users\zane4\Desktop\conway\example2.gif", writer=writergif)

#writermp4 = FFMpegWriter(fps=25, bitrate=3000)
#anim.save(r"C:\Users\zane4\Desktop\conway\example2.mp4", writer=writermp4)
```


