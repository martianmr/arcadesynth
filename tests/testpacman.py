"""Test all of the pac-man sounds"""

import pygame
import time
from arcadesynth import synth_pacman as pm

FREQUENCY = 44100
CHANNELS = 2

pygame.mixer.init(FREQUENCY, -16, CHANNELS)
pm.init(FREQUENCY, CHANNELS)
pygame.init()
credit = pygame.mixer.Sound(pm.pm_credit())
intro = pygame.mixer.Sound(pm.pm_intro())
siren1 = pygame.mixer.Sound(pm.pm_siren1())
siren2 = pygame.mixer.Sound(pm.pm_siren2())
siren3 = pygame.mixer.Sound(pm.pm_siren3())
siren4 = pygame.mixer.Sound(pm.pm_siren4())
siren5 = pygame.mixer.Sound(pm.pm_siren5())
wakka1 = pygame.mixer.Sound(pm.pm_wakka1())
wakka2 = pygame.mixer.Sound(pm.pm_wakka2())
energizer = pygame.mixer.Sound(pm.pm_energizer())
eat_ghost = pygame.mixer.Sound(pm.pm_eat_ghost())
eyes = pygame.mixer.Sound(pm.pm_eyes())
eat_fruit = pygame.mixer.Sound(pm.pm_eat_fruit())
extralife = pygame.mixer.Sound(pm.pm_extralife())
die = pygame.mixer.Sound(pm.pm_die())
intermission = pygame.mixer.Sound(pm.pm_intermission())

credit.play()
time.sleep(credit.get_length() * 2)
intro.play()
time.sleep(intro.get_length())
siren1.play(-1)
for _ in range(4):
    wakka1.play()
    time.sleep(wakka1.get_length() * 2)
    wakka2.play()
    time.sleep(wakka2.get_length() * 2)
siren1.stop()
for _ in range(8):
    energizer.play()
    time.sleep(energizer.get_length())
eat_ghost.play()
time.sleep(eat_ghost.get_length())
for _ in range(5):
    eyes.play()
    time.sleep(eyes.get_length())
for siren in siren2, siren3, siren4, siren5:
    for _ in range(2):
        siren.play()
        time.sleep(siren.get_length())
eat_fruit.play()
time.sleep(eat_fruit.get_length())
extralife.play()
time.sleep(extralife.get_length())
die.play()
time.sleep(die.get_length())
intermission.play()
time.sleep(intermission.get_length())