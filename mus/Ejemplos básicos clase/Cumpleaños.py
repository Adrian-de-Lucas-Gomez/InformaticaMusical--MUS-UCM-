# Ejercicio 7
# Alumnos: Andrés Ruiz Bartolomé , Adrián de Lucas Gómez


import pyaudio
import kbhit

from scipy.io import wavfile  # para manejo de wavs
import numpy as np  # arrays
from format_tools import *


SRATE = 44100
SEGUNDOS_POR_UNIDAD = 0.5

def osc(f, d):
    a = np.linspace(0, int((2*np.pi)*f*d), int(d * SRATE))
    a = np.sin(a)
    x = np.linspace(0, int(d*SRATE), int(d * SRATE))
    return x, a

letrasnotas = 'abcdefg'
notas = [440,493.883,523.251,587.33,659.255,698.456,783.991]

def songParser(song):

    arr = np.empty(0)

    for note in song:

        nombreNota = note[0].lower()

        frecuencia = notas[letrasnotas.index(nombreNota)]

        if not note[0].isupper():
            frecuencia *= 2

        x, frag = osc(frecuencia, note[1] * SEGUNDOS_POR_UNIDAD)

        arr = np.concatenate((arr, frag))


        sil = np.zeros(int(SRATE/10 * SEGUNDOS_POR_UNIDAD)) #Para que se note mas la diferencia entre notas

        arr = np.concatenate((arr, sil))

    return arr


song = [('G', 0.5), ('G', 0.5), ('a', 1), ('G', 1),
         ('c', 1), ('b', 2), ('G', 0.5), ('G', 0.5),
          ('a', 1), ('G', 1), ('d', 1), ('c', 2),
         ('G', 0.5), ('G', 0.5), ('g', 1), ('e', 1),
          ('c', 1), ('b', 1), ('a', 1), ('f', 0.5),
        ('f', 0.5), ('e', 1), ('c', 1), ('d', 1),
         ('c', 2)]


input("Pulsa enter para empezar a cantar el cumpleaños feliz :D")

data = songParser(song)
data = toFloat32(data)

# arrancamos pyAudio
p = pyaudio.PyAudio()

CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)


# En data tenemos la cancion completa, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK, dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c = ' '
while len(bloque > 0) and c != 'q':
    # nuevo bloque
    bloque = data[numBloque*CHUNK: numBloque*CHUNK+CHUNK]

    # pasamos al stream  haciendo conversion de tipo
    stream.write(bloque.astype(data.dtype).tobytes())

    if kb.kbhit():
        c = kb.getch()

    numBloque += 1
    print('.', end='')

kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()
