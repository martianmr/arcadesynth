"""Test all of the space invaders sounds"""

import pygame
import time
from arcadesynth import synth_spaceinvaders as si
from testutil import loadsound

FREQUENCY = 44100
CHANNELS = 2


def silence_1s():
    return si.tobytes(si.make_silence(1000))


def testspaceinvaders():
    print ("TESTING: space invaders")
    heartbeat = loadsound([si.si_march1, silence_1s, si.si_march2, silence_1s,
                           si.si_march3, silence_1s, si.si_march4, silence_1s], "heartbeat")
    playerfire = loadsound([si.si_playerfire], "playerfire")
    explosion = loadsound([si.si_explosion], "explosion")
    aliendie = loadsound([si.si_aliendie], "aliendie")
    ufo = loadsound([si.si_ufo], "ufo")
    ufodie = loadsound([si.si_ufodie], "ufodie")
    extralife = loadsound([si.si_extralife], "extralife")

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


def main():
    pygame.mixer.init(FREQUENCY, -16, CHANNELS)
    si.init(FREQUENCY, CHANNELS)
    pygame.init()
    testspaceinvaders()


if __name__ == "__main__":
    main()