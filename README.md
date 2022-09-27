# Conway's Game of Life - Example 1

| Animation |  Kernel   |
| --------- | --------- |
| <img src="https://github.com/ZaneL/Conway/blob/main/example1/animation.gif?raw=true" width="300">  | <img src="https://github.com/ZaneL/Conway/blob/main/example1/kernel.jpg?raw=true" width="300">  |


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
anim.save(r"C:\Users\zane4\Desktop\conway\example1\animation.gif", writer=writergif)

# Save kernel image
plt.imshow(kernel)
plt.savefig(r"C:\Users\zane4\Desktop\conway\example1\kernel.jpg")
```

# Conway's Game of Life - Example 2

| Animation |  Kernel   | Growth Function | 
| --------- | --------- | --------- |
| <img src="https://github.com/ZaneL/Conway/blob/main/example2/animation.gif?raw=true" width="300">  | <img src="https://github.com/ZaneL/Conway/blob/main/example2/kernel.jpg?raw=true" width="300">  | <img src="https://github.com/ZaneL/Conway/blob/main/example2/growth.jpg?raw=true" width="300">

```python
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
```

# Conway's Game of Life - Example 3

| Animation |  Kernel   | Growth Function | 
| --------- | --------- | --------- |
| <img src="https://github.com/ZaneL/Conway/blob/main/example3/animation.gif?raw=true" width="300">  | <img src="https://github.com/ZaneL/Conway/blob/main/example3/kernel.jpg?raw=true" width="300">  | <img src="https://github.com/ZaneL/Conway/blob/main/example3/growth.jpg?raw=true" width="300">

```python
###############################################################################
# Conway's Game of Life - Example 3
############################################################################### 

import numpy as np
from numpy import random
from scipy.signal import convolve2d
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Update frequency
T = 10

# Size of game grid
gridSizeX = 64
gridSizeY = 64

# Convolution kernel, used for determining the number of neighbors
xKernel, yKernel = np.meshgrid(list(range(-9, 10)), list(range(-9, 10)))
rKernel = np.sqrt(xKernel**2 + yKernel**2)
kernel = norm.pdf(rKernel, 5, 1.5)
kernel = kernel / np.sum(kernel)

# Random starting grid
mainGrid = random.rand(gridSizeX, gridSizeY)

# Setup plot window
fig = plt.figure(frameon=False)
image = plt.imshow(mainGrid)
plt.axis('off')

def growth(neighborGrid):
    mean = 0.135    #mean = 0.248
    std = 0.015     #std = 0.02
    return ((norm.pdf(neighborGrid, mean, std) / norm.pdf(mean, mean, std)) * 2) - 1

# Function to update the grid
def update(frame):
    global mainGrid
    
    # Use 2D convolution to determine the number of active cells around each target cell
    neighborGrid = convolve2d(mainGrid, kernel, mode='same', boundary='wrap')
    
    # Determine whether cells grow, shrink or stay the same
    mainGrid = np.clip(mainGrid + (1 / T) * growth(neighborGrid), 0, 1)
    
    # Update the plot image
    image.set_array(mainGrid)

# Run animation
anim = FuncAnimation(fig, update, interval=30, frames=1000, repeat=False)

# Save as gif
writergif = PillowWriter(fps=30)
anim.save(r"C:\Users\zane4\Desktop\conway\example3\animation.gif", writer=writergif)

# Save kernel image
plt.imshow(kernel)
plt.savefig(r"C:\Users\zane4\Desktop\conway\example3\kernel.jpg")

# Save the growth function
plt.clf()
x = np.arange(0, 1, 0.001)
plt.plot(x, growth(x), color='black')
plt.axhspan(0, 1, facecolor='green', alpha=0.2)
plt.axhspan(-1, 0, facecolor='red', alpha=0.2)
plt.savefig(r"C:\Users\zane4\Desktop\conway\example3\growth.jpg")
```
