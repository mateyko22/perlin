import random
import numpy as np
import matplotlib.pyplot as plt


# zad 1

def random_numbers(leng, s):
    a = []
    random.seed(s)
    for i in range(leng):
        a.append(round(random.random(), 4))
    return a


r_num = random_numbers(5, 31)
print(r_num)


def wykres(tab):
    a = []
    for i in range(len(tab)):
        a.append(i)
    plt.plot(a, tab)

def interpol(tab, x):
    pass


wykres(r_num)