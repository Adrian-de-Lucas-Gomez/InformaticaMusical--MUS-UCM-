# 1_numPy/playNumPy.py   reproductor con Chunks
import pyaudio, kbhit

from scipy.io import wavfile # para manejo de wavs
import numpy as np  # arrays    
from format_tools import *




# abrimos wav y recogemos frecMuestreo y array de datos
SRATE, data = wavfile.read('piano.wav')


# informacion de wav
print("Sample rate ",SRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len: ",data.shape[0])


# arrancamos pyAudio
p = pyaudio.PyAudio()

CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)

numBloque = 0
kb = kbhit.KBHit()
c= ' '
canPress = True;
while  c!= 'q': 
    
    # if len(bloque>0):
    #     # nuevo bloque
    #     bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]    

    #     # pasamos al stream  haciendo conversion de tipo 
    #     stream.write(bloque.astype(data.dtype).tobytes())
    #     numBloque += 1

    if kb.kbhit() and canPress:
        c = kb.getch()
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]    
        
        canPress = False
        # pasamos al stream  haciendo conversion de tipo 
        stream.write(bloque.astype(data.dtype).tobytes())
        numBloque += 1

    print('.',end='')

kb.set_normal_term()        
stream.stop_stream()
stream.close()
p.terminate()