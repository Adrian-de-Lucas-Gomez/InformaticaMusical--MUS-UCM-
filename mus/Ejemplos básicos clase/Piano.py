# Ejercicio 8
# Alumnos: Andrés Ruiz Bartolomé , Adrián de Lucas Gómez

import numpy as np
import kbhit
import sounddevice as sd
import soundfile as sf
from format_tools import *
from scipy.io import wavfile
import time

OrigSRATE = 0
SRATE = 0

CHUNK = 1024
char = ' '
elapsedTime = 0.1
previousTime = 0.0
canPress = True


notas = {   # Velocidad de reproducción de las notas partiendo de la muestras
    'C': 1.0, 'D': 1.12, 'E': 1.26, 'F': 1.33, 'G': 1.5, 'A': 1.68, 'B': 1.89,
}

def pianoKeyHit(keychar):
    global char
    global SRATE
    global previousTime
    global canPress
    global OrigSRATE

    char = keychar

    SRATE = OrigSRATE

    if time.time() - previousTime > elapsedTime:
        canPress = True
        previousTime = time.time()

    # Notas normales

    if char == 'z':
        SRATE *= notas['C'] 
    elif char == 'x':
        SRATE *= notas['D']
    elif char == 'c':
        SRATE *= notas['E']
    elif char == 'v':
        SRATE *= notas['F']
    elif char == 'b':
        SRATE *= notas['G']
    elif char == 'n':
        SRATE *= notas['A']
    elif char == 'm':
        SRATE *= notas['B']
    elif char == 'a':
        SRATE *= notas['C'] * 2.0
    elif char == 's':
        SRATE *= notas['D'] * 2.0
    elif char == 'd':
        SRATE *= notas['E'] * 2.0
    elif char == 'f':
        SRATE *= notas['F'] * 2.0
    elif char == 'g':
        SRATE *= notas['G'] * 2.0
    elif char == 'h':
        SRATE *= notas['A'] * 2.0
    elif char == 'j':
        SRATE *= notas['B'] * 2.0

    else : 
        SRATE = -1



    if SRATE == -1:
        return False, SRATE
    else: return True, SRATE
    



def main():
    global canPress
    global OrigSRATE

    srate, data = wavfile.read('piano.wav')
    OrigSRATE = srate
    SRATE = OrigSRATE
    

    # miramos formato de samples
    data = toFloat32(data)

    # En data tenemos el wav completo, ahora procesamos por bloques (chunks)
    bloque = np.arange(CHUNK,dtype=data.dtype)
    numBloque = data.shape[0]
    kb = kbhit.KBHit()
    c= ' '
    
    nSamples = 0

    stream = sd.OutputStream(
            samplerate = SRATE,            # frec muestreo 
            blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
            channels   = len(data.shape))  # num de canales

    tocoTecla = False


    while c != 'q':
        # nuevo bloque
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        # pasamos al stream haciendo conversion de tipo

        if kb.kbhit() & canPress:
            c = kb.getch()
            canPress = False
            numBloque = 0
            tocoTecla, SRATE = pianoKeyHit(c)

            

        if tocoTecla:
            # print(f"srate: {SRATE}")
            nSamples = CHUNK

            stream = sd.OutputStream(
            samplerate = SRATE,            # frec muestreo 
            blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
            channels   = len(data.shape))  # num de canales

            stream.start()

        while nSamples==CHUNK: 
            # numero de samples a procesar: CHUNK si quedan y si no, los que queden
            nSamples = min(CHUNK,data.shape[0] - (numBloque+1)*CHUNK)

            # nuevo bloque
            bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]

            # lo pasamos al stream
            stream.write(bloque) # escribimos al stream

            numBloque += 1

        stream.stop()

    kb.set_normal_term()
    stream.stop()

main()