# Source Library

The curated source library lives in `/audio/` as loudness-matched MP3s, shared by the
EQ and Compression modules. (This `/sources/` WAV plan is retired — kept only for this doc.)

Current library (all from the same session, loudness-matched):

| File                 | EQ picker name     | Usable range    |
|----------------------|--------------------|-----------------|
| drums.mp3            | Drums              | full range      |
| kick.mp3             | Kick               | 63 Hz – 4 kHz   |
| snare.mp3            | Snare              | 125 Hz – 16 kHz |
| bass.mp3             | Bass               | 63 Hz – 4 kHz   |
| acoustic-guitar.mp3  | Acoustic Guitar    | 125 Hz – 8 kHz  |
| vocal.mp3            | Lead Vocal         | 125 Hz – 8 kHz  |
| bg-vocals.mp3        | Background Vocals  | 125 Hz – 8 kHz  |

Planned additions (Level 3 program material, per the TET-3 syllabus — all run 125 Hz – 8 kHz):
speech English male (Kyle records), speech female + speech German (LibriVox public domain),
classical guitar + solo instruments (Musopen public domain), full mix (bounce of the stem song).

## Pipeline for new files

1. Pick a clean 15–30 s excerpt that loops musically.
2. Mono (instruments/speech), 44.1 kHz.
3. Loudness-match to the library: ffmpeg linear loudnorm to **−19 LUFS**, confirm no clipping
   (the trainer adds up to +12 dB of EQ on top).
4. Short edge fades (~4 ms) so the loop point doesn't click.
5. Encode MP3 (~160 kbps), drop in `/audio/`, add an entry to `SOURCE_LIBRARY` in
   `staging.html` (id, name, category, path, `range: [lo, hi]`), verify, promote.

`range` is where the source actually has energy — the picker shows it as a hint, and
future curriculum tasks will clamp their frequency pools to it.
