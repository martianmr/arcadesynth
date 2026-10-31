<a id="arcadesynth.synth"></a>

# arcadesynth.synth

functions to programmatically synthesize retro arcade sound effects

[source](../src/arcadesynth/synth.py)

<a id="arcadesynth.synth.sawtooth"></a>

#### sawtooth

```python
def sawtooth(phase, special=None)
```

Calculate amplitude for a sawtooth wave at the given phase

<a id="arcadesynth.synth.triangle"></a>

#### triangle

```python
def triangle(phase, special=None)
```

Calculate amplitude for a triangle wave at the given phase

<a id="arcadesynth.synth.square"></a>

#### square

```python
def square(phase, special=None)
```

Calculate amplitude for a square wave at the given phase

special can be specified as a cutoff for generating PWM

<a id="arcadesynth.synth.sin"></a>

#### sin

```python
def sin(phase, special=None)
```

Calculate amplitude for a sine wave at the given phase

special can be used to simulate lower precision math

<a id="arcadesynth.synth.init"></a>

#### init

```python
def init(frequency=FREQUENCY, channels=CHANNELS)
```

Set up sample rate, do this first to avoid using defaults

E.g. get these values from pygame with 'frequency, _, channels = pygame.mixer.get_init()'

<a id="arcadesynth.synth.get_init"></a>

#### get\_init

```python
def get_init()
```

Return the configured calculated sample rate

<a id="arcadesynth.synth.notehz"></a>

#### notehz

```python
def notehz(note)
```

For a given note e.g. "A4", return the frequency in Hz

<a id="arcadesynth.synth.samplept"></a>

#### samplept

```python
def samplept(func, i, f, harmonics=0, p=[], special=None)
```

Calculate amplitude of a sample for a buffer position

Given a function to calculate amplitude of a wave (func) for a buffer position (i)
and frequency (f) calculate and return the amplitude.
If harmonics is not zero also add in the amplitude of the given order of harmonics.
If frequency is not constant throughout the buffer, track the current phase during the
building process and pass the current phase of the primary and any harmonics through 
the list (p), otherwise phase can be calculated on the fly.

<a id="arcadesynth.synth.ms_to_samples"></a>

#### ms\_to\_samples

```python
def ms_to_samples(ms)
```

Convert time in milliseconds to number of samples

<a id="arcadesynth.synth.samples_to_ms"></a>

#### samples\_to\_ms

```python
def samples_to_ms(n)
```

Convert number of samples to time in milliseconds

<a id="arcadesynth.synth.tobytes"></a>

#### tobytes

```python
def tobytes(buf)
```

Convert buffer with range -1.0 to 1.0 to short signed integers then output as a byte stream

Use this to convert a sound held in internal format to a byte list for external processing, e.g. by
pygame.

<a id="arcadesynth.synth.boost"></a>

#### boost

```python
def boost(buf, gain)
```

Apply gain to buffer

<a id="arcadesynth.synth.reverse"></a>

#### reverse

```python
def reverse(buf)
```

Return backwards copy of the buffer

<a id="arcadesynth.synth.combine"></a>

#### combine

```python
def combine(buf1, buf2)
```

Combine 2 buffers giving average amplitude for each sample

<a id="arcadesynth.synth.add"></a>

#### add

```python
def add(target, source, offset=0)
```

Add the source sample to the target buffer

<a id="arcadesynth.synth.constrain"></a>

#### constrain

```python
def constrain(buf, lower, upper)
```

Clip a buffer to an upper and lower constraint

<a id="arcadesynth.synth.vmove"></a>

#### vmove

```python
def vmove(buf, amount)
```

Shift samples in the Y axis

<a id="arcadesynth.synth.fade"></a>

#### fade

```python
def fade(buf, a1, a2)
```

Change start and end amplitude and scale smoothly between

<a id="arcadesynth.synth.slice"></a>

#### slice

```python
def slice(buf, start, end)
```

Extract a section of a buffer with start and end times in ms

<a id="arcadesynth.synth.median_filter"></a>

#### median\_filter

```python
def median_filter(buf)
```

Perform a median filter

<a id="arcadesynth.synth.lowpass_filter"></a>

#### lowpass\_filter

```python
def lowpass_filter(buf, cutoff, order=6)
```

Apply a filter that progressively removes frequencies above the cutoff

<a id="arcadesynth.synth.highpass_filter"></a>

#### highpass\_filter

```python
def highpass_filter(buf, cutoff, order=6)
```

Apply a filter that progressively removes frequencies below the cutoff

<a id="arcadesynth.synth.new_buffer"></a>

#### new\_buffer

```python
def new_buffer(content=[])
```

Create a new buffer of floating point amplitudes

<a id="arcadesynth.synth.sequence"></a>

#### sequence

```python
def sequence(beatlen, notes, finetune=1.0)
```

Sequence notes to a buffer for creating music

'beatlen' is the length of each beat in the sequence in milliseconds.
'notes' is a list of notes, each element of the list is in the following format:
[note_name, start_beat, length_in_beats, velocity, creation_function]
The creation function must have the parameter format (ms, volume, frequency)
finetune can be used to make the notes consistently slightly sharp/flat.

<a id="arcadesynth.synth.make_sawtooth"></a>

#### make\_sawtooth

```python
def make_sawtooth(ms, vol=0.2, freq=140.0)
```

Make a sawtooth wave

<a id="arcadesynth.synth.make_triangle"></a>

#### make\_triangle

```python
def make_triangle(ms, vol=0.2, freq=140.0)
```

Make a triangle wave

<a id="arcadesynth.synth.make_square"></a>

#### make\_square

```python
def make_square(ms, vol=0.2, freq=140.0, pwm=None)
```

Make a square wave

<a id="arcadesynth.synth.make_sin"></a>

#### make\_sin

```python
def make_sin(ms=600, vol=0.4, freq=50.0, harmonics=0, precision=None)
```

Make a sine wave

<a id="arcadesynth.synth.make_white"></a>

#### make\_white

```python
def make_white(ms=600, vol=0.4, smooth=False)
```

Fill a buffer with random amplitudes to produce white noise

If smooth is False use values of 1.0 or -1.0 randomly to produce white noise similar to the SN76477 Complex Sound Generator chip,
otherwise generate purely random amplitudes which gives a more natural noise.

<a id="arcadesynth.synth.make_brown"></a>

#### make\_brown

```python
def make_brown(ms=600, vol=0.1, freq=150.0, order=1)
```

Apply a lowpass filter to white noise to produce brown noise

<a id="arcadesynth.synth.make_sweep"></a>

#### make\_sweep

```python
def make_sweep(ms=80,
               startf=1500.0,
               endf=400.0,
               shape=triangle,
               vol=1.0,
               repeat=0,
               harmonics=0,
               special=None)
```

Create a buffer that starts at frequency startf and ends at endf

If repeat is not zero the cycle goes from startf to endf and back to startf in repeat milliseconds and
continues to cycle until ms milliseconds have been filled.

<a id="arcadesynth.synth.make_silence"></a>

#### make\_silence

```python
def make_silence(ms=500)
```

Create a buffer filled with silence

<a id="arcadesynth.synth.pad"></a>

#### pad

```python
def pad(buf, length)
```

Pad out a buffer with zeroes to length

<a id="arcadesynth.synth.tremolo"></a>

#### tremolo

```python
def tremolo(buf, freq, intensity, shape=sin, special=None)
```

Modify a buffer in place so that amplitude increases and decreases according to shape and intensity

<a id="arcadesynth.synth.noisalise"></a>

#### noisalise

```python
def noisalise(buf, vol=1.0, gain=1.0)
```

Apply gain to buffer proportional to mean amplitude, useful for restoring a constant RMS after processing noise

<a id="arcadesynth.synth.envelope"></a>

#### envelope

```python
def envelope(buf, attack, decay, sustain, release, start=0, end=MAX_LEN)
```

Modify a buffer in place with an ADSR envelope

<a id="arcadesynth.synth.echo"></a>

#### echo

```python
def echo(buf, ms, vol)
```

Modify buffer in place to add a short delay to the sound

