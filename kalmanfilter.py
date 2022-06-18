import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
if __name__ == '__main__':
    z = np.linspace(0, 100, 100)
    for i in range(0, 100):
        noise = random.gauss(1, 10)
        z[i] = z[i]+noise
    x = np.array([[0], [0]])
    p = np.array([[1, 0], [0, 1]])
    f = np.array([[1, 1], [0, 1]])
    q = np.array([[0.001, 0], [0, 0.001]])
    h = np.array([1, 0])
    r = 1
    x1 = []
    x2 = []
    for i in range(0, 100):
        x_ = f*x
        p_ = f*p*f.T+q
        k = p_*h.T/(h*p_*h.T+r)
        x = x_+k*(z[i]-h*x_)
        p = (np.eye(2)-k*h)*p_
        x1.append(x[0][0])
        #x2.append(x[1])
    print(len(x1))
    y=[]
    for i in range(0, 100):
        y.append(i)
    plt.plot(y, x1)
    plt.plot(y, z)
    plt.show()

    