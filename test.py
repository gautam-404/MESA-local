import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
G = 6.67430e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the sun

# Initial conditions
N = 10000  # Number of particles
R = 10 * 149.6e6  # Initial disk radius
h = R / 10  # Smoothing length
mass = M_sun / N  # Mass of each particle

# Positions and velocities of particles
x = np.random.uniform(-R, R, (N, 3))
v = np.zeros((N, 3))

# Time step
dt = 0.01

# Iterate over time steps
for i in range(1000):
  # Compute acceleration for each particle
  a = np.zeros((N, 3))
  for j in range(N):
    for k in range(N):
      if j != k:
        r = x[j] - x[k]
        r_mag = np.linalg.norm(r)
        if r_mag < 2 * h:
          q = r_mag / h
          W = (10 / 7) * (1 - 1.5 * q**2 + 0.75 * q**3) / h**3
          a[j] += mass * W * G * (x[k] - x[j]) / r_mag**3

  # Update velocities and positions
  v += a * dt
  x += v * dt

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[:,0], x[:,1], x[:,2])
plt.show()
