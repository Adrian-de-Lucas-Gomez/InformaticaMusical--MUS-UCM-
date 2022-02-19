from pickle import NONE
from random import random
import numpy as np
import matplotlib.pyplot as plt
from sympy import fresnelc

SRATE = 44100
BUF_SIZE = 1024

def ej1():

    a= list(range(44100))
    b = np.random.rand(44100)
    b = b*2-1

    plt.plot(a,b)
    plt.show()

def ej2():

    a= list(range(2*44100))

    b = np.zeros(2*44100)

    i=0
    
    for valor in a:
        num = valor / (2*44100) * 6 * np.pi
        b[i] = np.sin(num)
        i = i + 1

    plt.plot(a,b)
    plt.show()

def ej3():

    a,b= osc(10,1)

    plt.plot(a,b)
    plt.show()

def osc(f,d):
    a= list(range(d*SRATE))

    b = np.zeros(d*SRATE)

    i=0
    
    for valor in a:
        num = valor / (d * SRATE) * 2 * f * np.pi
        b[i] = np.sin(num)
        i = i + 1

    return a,b

def vol(sample, vol):
    sample = sample * vol
    return sample

def modulaVol(sample, frec):
    sample = sample * frec
    return sample


def ej4():

    a,b= osc(1,1)
    c,d= osc(5,1)

    #b = vol(b, 0.5)
    b = modulaVol(b,d)

    plt.plot(a,b)
    plt.show()


def ej5():

    a,b= osc(10,2)

    b = fadeOut(b,1)

    plt.plot(a,b)
    plt.show()

def fadeOut(sample,t):

    s = len(sample) - t*SRATE

    z = np.ones(shape=(len(sample)-s))
    fade = np.arange(s)
    fade = s - fade
    fade = fade/s
    fade = np.append(z,fade)
    sample *= fade
    return sample

def osc(f,d):
    a= list(range(d*SRATE))

    b = np.zeros(d*SRATE)

    i=0
    
    for valor in a:
        num = valor / (d * SRATE) * 2 * f * np.pi
        b[i] = np.sin(num)
        i = i + 1

    return a,b

class Osc:

    def __init__(self, frec):
        self.f = frec
        self.nextTrack = 0


    def next(self):

        a= list(range(self.nextTrack*BUF_SIZE, self.nextTrack*BUF_SIZE + BUF_SIZE))

        b = np.zeros(BUF_SIZE)

        #44100 / BUF_SIZE

        i= 0
    
        for valor in a:
            num = valor / (SRATE) * 2 * self.f * np.pi
            b[i] = np.sin(num)
            i = i + 1

        self.nextTrack += 1

        return b


def ej6():
    
    o = Osc(100)

    b = [0.0]
    nextNum = 10

    for i in range(nextNum):
        baux = o.next()
        np.concatenate(b, baux)

    a = list(range(BUF_SIZE * nextNum))

    plt.plot(a,b)
    plt.show()



ej6()