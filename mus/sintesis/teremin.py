import pygame
from pygame.locals import *
WIDTH = 480
HEIGHT = 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")
...
# obtencion de la posicion del raton

jugando = True

while(jugando):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            print(mouseX, mouseY)
        if(event.type == pygame.QUIT):
            jugando = False
            
pygame.quit()