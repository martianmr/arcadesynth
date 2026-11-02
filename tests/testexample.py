"""Test all of the example sounds"""

import pygame
import time
from arcadesynth import synth_example as example
from testutil import loadsound

FREQUENCY = 44100
CHANNELS = 2

def testexample():
    print ("TESTING: example")
    gunshot = loadsound([example.eg_gunshot], "gunshot")
    boom = loadsound([example.eg_boom], "boom")
    zap = loadsound([example.eg_zap], "zap")

    gunshot.play()
    time.sleep(gunshot.get_length() * 1.5)
    boom.play()
    time.sleep(boom.get_length() * 1.5)
    zap.play()
    time.sleep(zap.get_length())


def main():
    pygame.mixer.init(FREQUENCY, -16, CHANNELS)
    example.init(FREQUENCY, CHANNELS)
    pygame.init()
    testexample()


if __name__ == "__main__":
    main()