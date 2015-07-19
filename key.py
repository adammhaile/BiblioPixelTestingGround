import pygame
from pygame.locals import *
import time, sys

done = False    

while not done:

    # get key current state
    keys = pygame.key.get_pressed()
    print keys
    if keys[K_SPACE]:
        #repeating fire while held
        print "Fire!"

    time.sleep(0.5)