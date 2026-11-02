from arcadesynth.synth import init
import pygame
import time
import array

FREQUENCY = 44100
CHANNELS = 2


def testinit(frequency=FREQUENCY, channels=CHANNELS):
    pygame.mixer.init(frequency, -16, channels)
    init(frequency, CHANNELS)
    pygame.init()


def loadsound(functions, name):
    allstart = time.time()
    buf = (array.array("h")).tobytes()
    for f in functions:
        start = time.time()
        buf += f()
        end = time.time()
        print("Loaded", f.__name__, "in", round(end - start, 6), "seconds")
    sound = pygame.mixer.Sound(buf)
    allend = time.time()
    print("Loaded", name, "in", round(allend - allstart, 6), "seconds, length", round(sound.get_length(), 2))
    return sound

