import numpy as np
T = np.array([[0.5,0.2],[0.5,0.8]])
b = np.array([[1],
              [0]])
for i in range(100):
    print(b)
    for j in range(100):
        b = np.dot(T,b)