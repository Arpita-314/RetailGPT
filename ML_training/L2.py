import numpy as np
import matplotlib.pyplot as plt

# Parameters for the Lorenz system
sigma = 10
rho = 28
beta = 8/3

# Lorenz system differential equations
def lorenz(x, y, z, sigma=sigma, rho=rho, beta=beta):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# Time parameters
dt = 0.01
num_steps = 10000

# Initial conditions
x, y, z = 0., 1., 1.05

# Arrays to hold the trajectory
xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)

xs[0], ys[0], zs[0] = x, y, z

# Integrate the Lorenz equations
for i in range(num_steps):
    dx, dy, dz = lorenz(x, y, z)
    x += dx * dt
    y += dy * dt
    z += dz * dt
    xs[i + 1] = x
    ys[i + 1] = y
    zs[i + 1] = z

# Create a 3D plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs, ys, zs, lw=0.5)

# Add title and labels
ax.set_title('Lorenz Attractor')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# Show the plotṇ
plt.show()
