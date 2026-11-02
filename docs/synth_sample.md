<a id="arcadesynth.synth_sample"></a>

# arcadesynth.synth\_sample

some simple basic sounds

[source](../src/arcadesynth/synth_sample.py)

<a id="arcadesynth.synth_sample.sawtooth_wave"></a>

#### sawtooth\_wave

```python
def sawtooth_wave(ms=500, vol=1.0, freq=150.0)
```

Return bytes representing a simple sawtooth wave

<a id="arcadesynth.synth_sample.triangle_wave"></a>

#### triangle\_wave

```python
def triangle_wave(ms=500, vol=1.0, freq=150.0)
```

Return bytes representing a simple triangle wave

<a id="arcadesynth.synth_sample.sine_wave"></a>

#### sine\_wave

```python
def sine_wave(ms=500, vol=1.0, freq=150.0)
```

Return bytes representing a simple sine wave

<a id="arcadesynth.synth_sample.square_wave"></a>

#### square\_wave

```python
def square_wave(ms=500, vol=1.0, freq=150.0)
```

Return bytes representing a simple square wave

<a id="arcadesynth.synth_sample.brown_noise"></a>

#### brown\_noise

```python
def brown_noise(ms=500, vol=1.0, freq=150.0)
```

Return bytes representing brown noise

<a id="arcadesynth.synth_sample.white_noise"></a>

#### white\_noise

```python
def white_noise(ms=500, vol=1.0, smooth=False)
```

Return bytes representing white noise

<a id="arcadesynth.synth_sample.sweep"></a>

#### sweep

```python
def sweep(ms=500, startf=1500.0, endf=100.0, shape=sin, vol=1.0, repeat=0)
```

Return bytes representing a frequency sweep from startf to endf

<a id="arcadesynth.synth_sample.chord"></a>

#### chord

```python
def chord(ms=500, vol=1.0, f1=notehz("C3"), f2=notehz("E3"))
```

Return bytes representing a 2 note chord

<a id="arcadesynth.synth_sample.fadeup"></a>

#### fadeup

```python
def fadeup(ms=500, a1=0.2, a2=1.0)
```

Return bytes representing a note that fades up in amplitude

<a id="arcadesynth.synth_sample.silence"></a>

#### silence

```python
def silence(ms=500)
```

Return bytes containing silence

