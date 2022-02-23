# ejercicio entregable: delay

import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs
import time

CHUNK = 1024 # tamanio del buffer
char = ' '
frec = 1.0
elapsedTime = 0.2
previousTime = 0.0
canPress = True
frequencies = [523.251,554.365,587.33,622.254,659.255,698.456,739.989,783.991,830.609,880,932.328,987.767]

def speedx(sound_array, factor):
    """ Multiplica la 'velocidad' de la muestra por un factor """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def keyboard_Proc(keychar, block, numBlock):
    """procesa las teclas del teclado que son parte del piano y devuelve el blocke correspondiente"""
    global char
    global frec
    global previousTime
    global canPress

    char = keychar

    if time.time() - previousTime > elapsedTime:
        canPress = True
        previousTime = time.time()

    # Notas normales

    if char == 'z':
        block *= 1.0
    elif char == 'x':
        block *= 1.12
    elif char == 'c':
        block *= 1.19
    elif char == 'v':
        block *= 1.33
    elif char == 'b':
        block *= 1.5
    elif char == 'n':
        block *= 1.59
    elif char == 'm':
        block *= 1.78

    # Notas normales

    if char == 'a':
        block *= 1.0 * 2.0
    elif char == 's':
        block *= 1.12 * 2.0
    elif char == 'd':
        block *= 1.19 * 2.0
    elif char == 'f':
        block *= 1.33 * 2.0
    elif char == 'g':
        block *= 1.5 * 2.0
    elif char == 'h':
        block *= 1.59 * 2.0
    elif char == 'j':
        block *= 1.78 * 2.0

    else: 
        numBlock = 1000000

    # block = speedx(block, frec)

    numBlock+=1
    return numBlock, block

def main():
    srate, data = wavfile.read('piano.wav')

    global SRATE
    global canPress
    SRATE = srate

    # miramos formato de samples
    if data.dtype.name == 'int16': fmt = 2
    elif data.dtype.name == 'int32': fmt = 4
    elif data.dtype.name == 'float32': fmt = 4
    elif data.dtype.name == 'uint8': fmt = 1
    else: raise Exception('Not supported')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
    channels=len(data.shape), # num canales (shape de data)
    rate=SRATE, # frecuencia de muestreo
    frames_per_buffer=CHUNK, # tamanio buffer
    output=True)

    # En data tenemos el wav completo, ahora procesamos por bloques (chunks)
    bloque = np.arange(CHUNK,dtype=data.dtype)
    numBloque = data.shape[0]
    kb = kbhit.KBHit()
    c= ' '

    while c != 'q':
        # nuevo bloque
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        # pasamos al stream haciendo conversion de tipo

        if kb.kbhit() & canPress:
            c = kb.getch()
            canPress = False
            numBloque = 0
            
        numBloque, block = keyboard_Proc(c, bloque, numBloque)

        stream.write(block.astype((data.dtype)).tobytes())

        numBloque += 1

    kb.set_normal_term()
    stream.stop_stream()
    stream.close()
    p.terminate()

main()