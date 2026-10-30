"""Test all of the asteroids sounds"""

import pygame
import time
from arcadesynth import synth_asteroids as asteroids

FREQUENCY = 44100
CHANNELS = 2

pygame.mixer.init(FREQUENCY, -16, CHANNELS)
asteroids.init(FREQUENCY, CHANNELS)
pygame.init()
heartbeat = pygame.mixer.Sound(asteroids.as_bump1() + asteroids.tobytes(asteroids.make_silence(1000)) + asteroids.as_bump2() + asteroids.tobytes(asteroids.make_silence(1000)))
playerfire = pygame.mixer.Sound(asteroids.as_playerfire())
explode_large = pygame.mixer.Sound(asteroids.as_explode_large())
explode_medium = pygame.mixer.Sound(asteroids.as_explode_medium())
explode_small = pygame.mixer.Sound(asteroids.as_explode_small())
thrust = pygame.mixer.Sound(asteroids.as_thrust())
extralife = pygame.mixer.Sound(asteroids.as_extralife())
ufo_large = pygame.mixer.Sound(asteroids.as_ufo_large())
ufo_small = pygame.mixer.Sound(asteroids.as_ufo_small())
ufo_fire = pygame.mixer.Sound(asteroids.as_ufofire())

heartbeat.play(-1)
time.sleep(0.6)
thrust.play(-1)
time.sleep(1.6)
thrust.stop()
time.sleep(0.6)
for f in explode_large, explode_medium, explode_small:
    playerfire.play()
    time.sleep(0.75)
    f.play()
    time.sleep(0.5)
time.sleep(0.1)
for f in ufo_large, ufo_small:
    f.play(-1)
    for _ in range(5):
        ufo_fire.play()
        time.sleep(ufo_fire.get_length() * 3)
    f.stop()
    time.sleep(0.6)
extralife.play()
time.sleep(extralife.get_length())
heartbeat.stop()