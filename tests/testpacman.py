"""Test all of the pac-man sounds"""

import pygame
import time
from arcadesynth import synth_pacman as pm
from testutil import loadsound

FREQUENCY = 44100
CHANNELS = 2


def testpacman():
    print ("TESTING: pac-man")
    credit = loadsound([pm.pm_credit], "credit")
    intro = loadsound([pm.pm_intro], "intro")
    siren1 = loadsound([pm.pm_siren1], "siren1")
    siren2 = loadsound([pm.pm_siren2], "siren2")
    siren3 = loadsound([pm.pm_siren3], "siren3")
    siren4 = loadsound([pm.pm_siren4], "siren4")
    siren5 = loadsound([pm.pm_siren5], "siren5")
    wakka1 = loadsound([pm.pm_wakka1], "wakka1")
    wakka2 = loadsound([pm.pm_wakka2], "wakka2")
    energizer = loadsound([pm.pm_energizer], "energizer")
    eat_ghost = loadsound([pm.pm_eat_ghost], "eat_ghost")
    eyes = loadsound([pm.pm_eyes], "eyes")
    eat_fruit = loadsound([pm.pm_eat_fruit], "eat_fruit")
    extralife = loadsound([pm.pm_extralife], "extralife")
    die = loadsound([pm.pm_die], "die")
    intermission = loadsound([pm.pm_intermission], "intermission")

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


def main():
    pygame.mixer.init(FREQUENCY, -16, CHANNELS)
    pm.init(FREQUENCY, CHANNELS)
    pygame.init()
    testpacman()


if __name__ == "__main__":
    main()