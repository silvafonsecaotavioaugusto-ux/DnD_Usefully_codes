import numpy as np

def f(x):
    return -3*np.exp(-x) + 3

x = 1
y = f(x)
n = 0
while abs(x - y) > 0.00001:
    x -= 0.1 * (x -y)
    y = f(x)
    n += 1
    if n > 10000:
        break
print(f'{y:.3f}')