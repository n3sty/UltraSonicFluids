# Luuk 23-nov
# let op dit is nog een test voor een betere animatie manier nog niet af
# https://www.youtube.com/watch?app=desktop&v=Ercd-Ip5PfQ

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


def ani_plot_initilize():
    """
    #plots the data in real time
    """
    x_var = []
    y_var = []

    index = count()


def plot_animate(i):
    x_var.append(next(index))
    y_var.append(random.randint(0, 5))

    plt.plot(x_var, y_var)




animate = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
