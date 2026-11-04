"""Test all of the sample sounds"""

import pygame
import time
from arcadesynth import synth_sample as sample
from testutil import loadsound

FREQUENCY = 44100
CHANNELS = 2

def testsample():
    print ("TESTING: sample")
    sawtooth_wave = loadsound([sample.sawtooth_wave], "sawtooth_wave")
    triangle_wave = loadsound([sample.triangle_wave], "triangle_wave")
    sine_wave = loadsound([sample.sine_wave], "sine_wave")
    square_wave = loadsound([sample.square_wave], "square_wave")
    brown_noise = loadsound([sample.brown_noise], "brown_noise")
    white_noise = loadsound([sample.white_noise], "white_noise")
    sweep = loadsound([sample.sweep], "sweep")
    chord = loadsound([sample.chord], "chord")
    fadeup = loadsound([sample.fadeup], "fadeup")
    silence = loadsound([sample.silence], "silence")

    sawtooth_wave.play()
    time.sleep(sawtooth_wave.get_length() * 1.5)
    triangle_wave.play()
    time.sleep(triangle_wave.get_length() * 1.5)
    sine_wave.play()
    time.sleep(sine_wave.get_length() * 1.5)
    square_wave.play()
    time.sleep(square_wave.get_length() * 1.5)
    brown_noise.play()
    time.sleep(brown_noise.get_length() * 1.5)
    white_noise.play()
    time.sleep(white_noise.get_length() * 1.5)
    sweep.play()
    time.sleep(sweep.get_length() * 1.5)
    chord.play()
    time.sleep(chord.get_length() * 1.5)
    fadeup.play()
    time.sleep(fadeup.get_length() * 1.5)
    silence.play()
    time.sleep(silence.get_length())

def main():
    pygame.mixer.init(FREQUENCY, -16, CHANNELS)
    sample.init(FREQUENCY, CHANNELS)
    pygame.init()
    testsample()


if __name__ == "__main__":
    main()