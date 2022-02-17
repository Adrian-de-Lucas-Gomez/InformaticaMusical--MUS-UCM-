# 1_numPy/playNumPy.py   reproductor con Chunks
import pyaudio
import kbhit

from scipy.io import wavfile  # para manejo de wavs
import numpy as np  # arrays
from format_tools import *


SRATE = 44100


def osc(f, d):
    a = np.linspace(0, int((2*np.pi)*f*d), int(d * SRATE))
    a = np.sin(a)
    x = np.linspace(0, int(d*SRATE), int(d * SRATE))
    return x, a


def songParser(song):

    arr = np.empty(0)

    for note in song:

        nombreNota = note[0].lower()
        frecuencia = 0

        if nombreNota == 'g':
            frecuencia = 783.991
        elif nombreNota == 'a':
            frecuencia = 880
        elif nombreNota == 'b':
            frecuencia = 987.767
        elif nombreNota == 'c':
            frecuencia = 523.251
        elif nombreNota == 'd':
            frecuencia = 587.33
        elif nombreNota == 'e':
            frecuencia = 659.255
        elif nombreNota == 'f':
			frecuencia = 698.456

		if not note[0].isupper():
			frecuencia /= 2

		x, frag = osc(frecuencia, note[1])

		x,sil = osc(1, 0.1)

        arr = np.concatenate((arr, frag))
        arr = np.concatenate((arr, frag))

    return arr


x, a = osc(100, 10)

# abrimos wav y recogemos frecMuestreo y array de datos
# SRATE, data = wavfile.read('piano.wav')

# data = a
# data = toFloat32(data)

song = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1),
 		('c', 1), ('B', 2), ('G', 0.5), ('G', 0.5),
		  ('A', 1), ('G', 1), ('d', 1), ('c', 2),
		 ('G', 0.5), ('G', 0.5), ('g', 1), ('e', 1),
		  ('c', 1), ('B', 1), ('A', 1), ('f', 0.5),
        ('f', 0.5), ('e', 1), ('c', 1), ('d', 1),
		 ('c', 2)]

debugSong = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1)]

data = songParser(debugSong)
data = toFloat32(data)

# # informacion de wav
# print("Sample rate ", SRATE)
# print("Sample format: ", data.dtype)
# print("Num channels: ", len(data.shape))
# print("Len: ", data.shape[0])


# arrancamos pyAudio
p = pyaudio.PyAudio()

CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
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
