import pygame
import time
from arcadesynth import synth_pacman as pm

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound(pm.pm_siren_low())
sound1 = pygame.mixer.Sound(pm.pm_wakka1())
sound2 = pygame.mixer.Sound(pm.pm_wakka2())
sound.play(-1)
for _ in range(10):
    sound1.play()
    time.sleep(0.16)
    sound2.play()
    time.sleep(0.16)