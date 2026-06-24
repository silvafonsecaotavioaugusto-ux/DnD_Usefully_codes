import numpy as np
import matplotlib.pyplot as plt



#distribuição para 1d4 + 1d10
def n_4_10_rolls(n: int = 0):
    if n == 0:
        print("No number of rolls was given!")
    else:
       d4 = np.random.randint(low= 1, high= 5, size= n)
       d10 = np.random.randint(low= 1, high= 11, size= n)
       result = d4 + d10
       return result

#distribuição para 1d6 + 1d8
def n_6_8_rolls(n: int = 0):
    if n == 0:
        print("No number of rolls was given!")
    else:
        d6 = np.random.randint(low= 1, high= 7, size= n)
        d8 = np.random.randint(low= 1, high= 9, size= n)
        result = d6 + d8
        return result

#distribuição de 1d12
def n_12_rolls(n: int = 0):
    if n == 0:
        print("No number of rolls was given!")
    else:
        d12 = np.random.randint(low= 1, high= 13, size= n)
        return d12

#distribuição de 2d6
def n_6_6_rolls(n: int = 0):
    if n == 0:
        print("No number of rolls was given!")
    else:
        d6_1 = np.random.randint(low= 1, high= 7, size= n)
        d6_2 = np.random.randint(low= 1, high= 7, size= n)
        result = d6_1 + d6_2
        return result


m = 100000000
dist_6_8 = n_6_8_rolls(m)
dist_4_10 = n_4_10_rolls(m)
dist_6_6 = n_6_6_rolls(m)
dist_12 = n_12_rolls(m)

y_max_1 = 0.18
y_max_2 = 0.11

fig1 = plt.figure()
ax, ay = fig1.add_subplot(121), fig1.add_subplot(122)
ax.hist(dist_12, bins= range(1,14), density=True)
ax.set_title("Distribuição de 1d12")
ax.set_ylim(ymin=0, ymax= y_max_2)
ay.hist(dist_4_10, bins=range(2, 16), density=True)
ay.set_title("Distribuição de 1d4 + 1d10")
ay.set_ylim(ymin=0, ymax= y_max_2)

fig2 = plt.figure()
aw, az = fig2.add_subplot(121), fig2.add_subplot(122)
aw.hist(dist_6_6, bins= range(2,14), density=True)
aw.set_title("Distribuição de 2d6")
aw.set_ylim(ymin=0, ymax= y_max_1)
az.hist(dist_6_8, bins=range(2, 16), density=True)
az.set_title("Distribuição d6 + d8")
az.set_ylim(ymin=0, ymax= y_max_1)

plt.show()