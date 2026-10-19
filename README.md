# arcadesynth 1.0.2

Programmatically synthesize retro arcade sound effects with arcadesynth

This utility can be used to generate your own custom sound effects in code as an alternative to using sound assets. It also provides some hand-crafted sounds from the Golden age of arcade video games.

The idea was inspired by sound generation on 1980s 8-bit microcomputers which sometimes had fairly sophisticated synthesizer chips which could be programmed at a low level with a bit of know-how. The algorithms are kept fairly simple but are capable of approximating early arcade, console and computer game sounds that are generated with specialized chips or custom electronics.

## Installation

arcadesynth can be installed via pip

```bash
pip install arcadesynth
```

## Modules

- synth - functions to build your own effects
- synth_sample - some simple basic sounds
- synth_example - some generic retro sound effects
- synth_asteroids - sounds from the 1979 Atari game Asteroids
- synth_spaceinvaders - sounds from the 1978 Taito game Space Invaders

## Synth

This module can be used to create custom sound effects by generating waves or white noise and then manipulating the signal with envelopes, filters and more.

E.g. synthesize a retro gunshot sound in pygame.

```python
import pygame
from arcadesynth import synth

pygame.init()
pygame.mixer.init()
ms = 500 # Length of buffer will be 500 milliseconds
buf = synth.make_white(ms, 1.0) # Fill buffer with white noise
buf = synth.lowpass_filter(buf, 1200.0, order=4) # Apply a filter to remove higher frequencies
synth.noisalise(buf, gain=0.5) # Even out the amplitude of the noise
synth.envelope(buf, 20, 30, 0.2, ms - 50) # Apply an envelope with a short attack and decay and then fade off from 20% amplitude
sound = pygame.mixer.Sound(synth.tobytes(buf))
sound.play()
```

## Space Invaders

There are some built-in hand-crafted synthesized sounds including those from the 1978 classic Space Invaders by Taito. Sounds in the arcade machine are produced on a Texas Instruments SN76477 'complex sound generator' chip supported by custom electronics. 

E.g. synthesize the sound made by the flying saucer blowing up in Space Invaders.

```python
import pygame
from arcadesynth import synth_spaceinvaders as si

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound(si.si_ufodie())
sound.play()
```

## LICENSE

MIT License — See the [LICENSE](LICENSE) file for details.