import pygame
import sys
import wave

from arcadesynth import synth_asteroids as ast
from arcadesynth import synth_spaceinvaders as si
from arcadesynth import synth_pacman as pm

FREQUENCY = 44100
CHANNELS = 1
_sound_ok = False
WHITE = (255, 255, 255)

def init_audio():
    """Initialise the mixer and build all game sounds."""
    global _sound_ok
    try:
        pygame.mixer.init()
        frequency, _, channels = pygame.mixer.get_init()
        ast.init(frequency, channels)
        _sound_ok = True
    except pygame.error:
        _sound_ok = False

class Game:
    def __init__(self):
        print("Init started")
        self.screen = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()
        init_audio()
        self.sound = pygame.mixer.Sound(si.si_extralife())
        sfile = wave.open('output.wav', 'w')
        sfile.setframerate(FREQUENCY)
        sfile.setnchannels(CHANNELS)
        sfile.setsampwidth(2)
        sfile.writeframesraw(self.sound.get_raw())
        sfile.close()
        self.sound.set_volume(0.5)
        print("Init done")


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                print(pygame.mixer.get_init())
                print(self.sound.get_length())
                self.sound.play()
        return True

    def draw(self):
        self.screen.fill(WHITE)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        pygame.quit()
        sys.exit()


def main():
    pygame.mixer.pre_init(frequency=FREQUENCY, channels = CHANNELS)
    pygame.init()
    Game().run()


if __name__ == "__main__":
    main()
