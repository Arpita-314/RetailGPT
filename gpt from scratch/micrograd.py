import numpy as np
import matplotlib.pyplot as plt
import math
*matplotlib inline

def f(x):
    return 3*x**2 - 4*x + 5

f(3.0)

xs = np.arange(-5, 5, 0.25)
ys = f(xs)
plt.plot(xs, ys)

h = 0.001
x = 3.0
f(x + h)

