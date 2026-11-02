"""Test all of the asteroids sounds"""

import pygame
import time
from arcadesynth import synth_asteroids as asteroids
from testutil import loadsound

FREQUENCY = 44100
CHANNELS = 2

def silence_1s():
    return asteroids.tobytes(asteroids.make_silence(1000))

def testasteroids():
    print ("TESTING: asteroids")
    heartbeat = loadsound([asteroids.as_bump1, silence_1s, asteroids.as_bump2, silence_1s], "heartbeat")
    playerfire = loadsound([asteroids.as_playerfire], "playerfire")
    explode_large = loadsound([asteroids.as_explode_large], "explode_large")
    explode_medium = loadsound([asteroids.as_explode_medium], "explode_medium")
    explode_small = loadsound([asteroids.as_explode_small], "explode_small")
    thrust = loadsound([asteroids.as_thrust], "thrust")
    extralife = loadsound([asteroids.as_extralife], "extralife")
    ufo_large = loadsound([asteroids.as_ufo_large], "ufo_large")
    ufo_small = loadsound([asteroids.as_ufo_small], "ufo_small")
    ufo_fire = loadsound([asteroids.as_ufofire], "ufo_fire")

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
        for _ in range(3):
            ufo_fire.play()
            time.sleep(ufo_fire.get_length() * 3)
        f.stop()
        time.sleep(0.6)
    extralife.play()
    time.sleep(extralife.get_length())
    heartbeat.stop()


def main():
    pygame.mixer.init(FREQUENCY, -16, CHANNELS)
    asteroids.init(FREQUENCY, CHANNELS)
    pygame.init()
    testasteroids()


if __name__ == "__main__":
    main()