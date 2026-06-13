# Source Material Library

Drop the following WAV files in this directory to populate the Source Material picker
in the full version of Ear Training Lab. Filenames must match exactly.

| Filename                 | Category | Notes                                       |
|--------------------------|----------|---------------------------------------------|
| kick.wav                 | Drums    | Solo kick loop                              |
| snare.wav                | Drums    | Solo snare loop                             |
| hihat.wav                | Drums    | Closed hi-hat pattern                       |
| drum-bus.wav             | Drums    | Full kit / bus                              |
| bass-di.wav              | Bass     | DI bass, no amp/cab                         |
| electric-guitar.wav      | Guitar   | Clean or lightly-driven electric            |
| acoustic-guitar.wav      | Guitar   | Strummed or fingerpicked acoustic           |
| male-vocal.wav           | Vocal    | Solo male vocal phrase                      |
| female-vocal.wav         | Vocal    | Solo female vocal phrase                    |
| full-mix.wav             | Mix      | Polished full mix at -1 dBTP or so          |

## Recommended specs

- **Format**: uncompressed WAV (mono or stereo).
- **Sample rate**: 44.1 kHz.
- **Bit depth**: 16- or 24-bit.
- **Length**: 2–6 seconds. The clip loops in the engine, so make the loop point clean.
- **Level**: normalize to around **−6 dBFS peak**. The training applies up to +12 dB
  of EQ boost on top of the source — anything hotter than −6 dBFS will clip when
  filtered.
- **Mono vs stereo**: either is fine. Mono is preferred for instruments so the EQ
  changes are unambiguous; full mixes can stay stereo.

## Adding new sources

To add a new source, edit `SOURCE_LIBRARY` in `full.html` and
drop the WAV in this directory.
