# Ejercicio 10
# Alumnos: Andrés Ruiz Bartolomé , Adrián de Lucas Gómez

import pyaudio
import kbhit
import time
import format_tools
import numpy as np

# Variables de formato
CHUNK = 1024  # [16 a 1024] (Solo numeros pares)
CHANNELS = 1
RATE = 44100
HALF_CHUNK = int(CHUNK/2)

# Arrays para la reproduccion
bloque = np.zeros([CHUNK])
frames = np.array([]).astype(np.float32)

# Variables de Tiempo
lastTime = time.time()
currentTime = time.time()
delay = 0.5
# -------------------------


# Funcion callback que almacena en frames el audio recogido
def inputCallback(in_data, frame_count, time_info, status):
    global frames
    frames = np.append(frames, np.frombuffer(in_data))
    print(frames.shape)

    return (None, pyaudio.paContinue)

# Funcion callback para el flujo de salida que comprueba si el tiempo trancurrido
# es mayor al delay que hemos escogido y si es así reproduce el audio grabado
# y lo elimina de la lista "frames"


def outputCallback(in_data, frame_count, time_info, status):
    currentTime = time.time()

    if lastTime + delay < currentTime:
        global frames
        global bloque
        bloque = frames[HALF_CHUNK: HALF_CHUNK + HALF_CHUNK]
        frames = np.delete(frames, np.s_[HALF_CHUNK: HALF_CHUNK + HALF_CHUNK])

    return (bloque.astype(frames.dtype).tobytes(), pyaudio.paContinue)


def main():
    # Obtenemos el formato de los samples
    dataWidth = format_tools.getWidthData(frames)

    # Inicializamos PyAudio
    p = pyaudio.PyAudio()

    print("Bienvenido al idiotizador! Pulsa q para salir")

    # Abrimos un flujo de entrada de audio con funcion de callback para así no bloquear
    # la ejecucion del resto del programa
    inputStream = p.open(format=p.get_format_from_width(dataWidth),
                         channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK,
                         stream_callback=inputCallback)

    # Abrimos otro flujo pero esta vez de salida de audio con funcion de callback tambien
    outputStream = p.open(format=p.get_format_from_width(dataWidth),
                          channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, output=True,
                          stream_callback=outputCallback)

    # Inicializamos ambos flujos para que empiecen a funcionar
    inputStream.start_stream()
    outputStream.start_stream()

    # Mientras no se pulse la "q" seguimos
    kb = kbhit.KBHit()
    c = ' '
    while c != 'q':
        if kb.kbhit():
            c = kb.getch()
        time.sleep(0.1)

    # Cerramos todo
    kb.set_normal_term()
    inputStream.stop_stream()
    inputStream.close()
    outputStream.stop_stream()
    outputStream.close()
    p.terminate()
    input("Idiotizador cerrado, pulsa intro para salir")

main()
