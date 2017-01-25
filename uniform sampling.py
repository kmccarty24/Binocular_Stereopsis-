import matplotlib.pyplot as plt
import numpy as np
rad = 10
num = 10000000

t = np.random.uniform(0.0, 2.0*np.pi, num)
r = rad * np.sqrt(np.random.uniform(0.0, 1.0, num))
x = r * np.cos(t)
y = r * np.sin(t)
print t
plt.plot(x, y, "ro", ms=1)
plt.axis([-15, 15, -15, 15])
plt.show()

# rad = 5
# numb = 1000
# t = np.random.uniform(0.0, 2.0*np.pi, num) angle betwnn 0-2pi which is a cicle ?
# r = rad * np.sqrt(np.random.uniform(0.0, 1.0, num)) the sqrt gets rid of the clustering by making the smaller numbers more sparse
# x = r * np.cos(t)
# y = r * np.sin(t)

# dot_arrayUni = []
# for i in range(len(x)):
#     dot_arrayUni.append([x[i], y[i]])
