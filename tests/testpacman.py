import pygame
import time
from arcadesynth import synth_pacman as pm

pygame.mixer.init(44100, -16, 2)
pm.init(44100, 2)
pygame.init()
siren1 = pygame.mixer.Sound(pm.pm_siren1())
wakka1 = pygame.mixer.Sound(pm.pm_wakka1())
wakka2 = pygame.mixer.Sound(pm.pm_wakka2())
energizer = pygame.mixer.Sound(pm.pm_energizer())
eat_ghost = pygame.mixer.Sound(pm.pm_eat_ghost())
eyes = pygame.mixer.Sound(pm.pm_eyes())
siren1.play(-1)
for _ in range(5):
    wakka1.play()
    time.sleep(0.16)
    wakka2.play()
    time.sleep(0.16)
siren1.stop()
t = energizer.get_length()
for _ in range(10):
    energizer.play()
    time.sleep(t)
t = eat_ghost.get_length()
eat_ghost.play()
time.sleep(t)
t = eyes.get_length()
for _ in range(5):
    eyes.play()
    time.sleep(t)
