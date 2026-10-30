"""Test all of the space invaders sounds"""

import pygame
import time
from arcadesynth import synth_spaceinvaders as si

FREQUENCY = 44100
CHANNELS = 2

pygame.mixer.init(FREQUENCY, -16, CHANNELS)
si.init(FREQUENCY, CHANNELS)
pygame.init()
heartbeat = pygame.mixer.Sound(si.si_march1() + si.tobytes(si.make_silence(1000)) + si.si_march2() + si.tobytes(si.make_silence(1000)) +
                               si.si_march3() + si.tobytes(si.make_silence(1000)) + si.si_march4() + si.tobytes(si.make_silence(1000)))
playerfire = pygame.mixer.Sound(si.si_playerfire())
explosion = pygame.mixer.Sound(si.si_explosion())
aliendie = pygame.mixer.Sound(si.si_aliendie())
ufo = pygame.mixer.Sound(si.si_ufo())
ufodie = pygame.mixer.Sound(si.si_ufodie())
extralife = pygame.mixer.Sound(si.si_extralife())

heartbeat.play(-1)
time.sleep(0.6)
for _ in range(2):
    playerfire.play()
    time.sleep(0.2)
    aliendie.play()
    time.sleep(0.75)
for _ in range(2):
    playerfire.play()
    time.sleep(playerfire.get_length() * 2)
ufo.play(-1)
time.sleep(ufo.get_length() * 12)
ufo.stop()
ufodie.play()
time.sleep(ufodie.get_length())
time.sleep(0.6)
extralife.play()
time.sleep(extralife.get_length() * 2)
explosion.play()
time.sleep(explosion.get_length())
heartbeat.stop()