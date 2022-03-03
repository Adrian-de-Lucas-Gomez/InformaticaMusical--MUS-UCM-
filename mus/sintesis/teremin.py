# Ejercicio 3
# Alumnos: Andrés Ruiz Bartolomé , Adrián de Lucas Gómez
from sqlalchemy import Float
import pygame
from pygame.locals import *
import numpy as np         # arrays
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit
import os

WIDTH = 980
HEIGHT = 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 16


'''
# fc, carrier = pitch, fm frecuencia moduladora, beta = indice de modulacion
def oscFM(fc,fm,beta,vol,frame):
    # sin(2πfc+βsin(2πfm))   http://www.mrcolson.com/2016/04/21/Simple-Python-FM-Synthesis.html
    interval = np.arange(CHUNK)+frame
    mod = beta*np.sin(2*np.pi*fm*interval/RATE)
    res = np.sin(2*np.pi*fc*interval/RATE + mod)
    return (vol*res).astype(np.float32)
'''

# [(fc,vol),(fm1,beta1),(fm2,beta2),...]


def oscFM(frecs, frame):
    # sin(2πfc+βsin(2πfm))
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso

    for i in range(len(frecs)-1, -1, -1):
        samples = frecs[i][1] * \
            np.sin(2*np.pi*frecs[i][0]*chunk/SRATE + samples)
    return samples

    '''
    mod = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/RATE)
    res = np.sin(2*np.pi*fc*interval/RATE + mod)
    return (vol*res).astype(np.float32)
    '''


stream = sd.OutputStream(samplerate=SRATE, blocksize=CHUNK, channels=1)
stream.start()

kb = kbhit.KBHit()
c = ' '


# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
#frecs = [[220,0.8],[220,0.5],[110,0.3]]

fc, fm = 220, 220
frecs = [[fc, 0.8]]
frecRange = [100, 10000]

frame = 0

jugando = True

vol = 1
mouseX = 0
mouseY = 0

while(jugando):

    samples = oscFM(frecs, frame)
    stream.write(np.float32(vol*samples))

    frame += CHUNK

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            print(mouseX, mouseY)
        if(event.type == pygame.QUIT):
            jugando = False


    frecs[0][0] = (mouseX/WIDTH)*(frecRange[1]-frecRange[0]) + frecRange[0]
    vol = float(mouseY)/ HEIGHT 
    print(f"frecuencia {frecs[0][1]} volumen {vol}")


stream.stop()
pygame.quit()
