import time
import numpy as np

lst = []
while True:
    time.sleep(3)
    x = np.random.rand()
    x = round(x, 3)
    lst.append(x)
    lst[:-1] = lst[1:]
    lst[:-1].append(x)
    print(lst)
