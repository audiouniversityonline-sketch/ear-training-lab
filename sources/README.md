# Source Library

The curated source library lives in `/audio/` as loudness-matched MP3s, shared by the
EQ and Compression modules. (This `/sources/` WAV plan is retired — kept only for this doc.)

Current library (all from the same session, loudness-matched):

| File                    | EQ picker name     | Category         | Usable range    |
|-------------------------|--------------------|------------------|-----------------|
| course-acoustic.mp3     | Acoustic           | Course Files     | 125 Hz – 4 kHz  |
| course-first-timer.mp3  | First Timer        | Course Files     | full range      |
| course-me-vs-world.mp3  | Me vs World        | Course Files     | full range      |
| course-strings.mp3      | Strings            | Course Files     | 125 Hz – 8 kHz  |
| drums.mp3               | Drums              | Drums            | full range      |
| kick.mp3                | Kick               | Drums            | 63 Hz – 4 kHz   |
| snare.mp3               | Snare              | Drums            | 125 Hz – 16 kHz |
| bass.mp3                | Bass               | Bass             | 63 Hz – 4 kHz   |
| acoustic-guitar.mp3     | Acoustic Guitar    | Guitar           | 125 Hz – 8 kHz  |
| vocal.mp3               | Lead Vocal         | Vocals           | 125 Hz – 8 kHz  |
| bg-vocals.mp3           | Background Vocals  | Vocals           | 125 Hz – 8 kHz  |
| piano-chopin.mp3        | Piano              | Solo Instruments | 125 Hz – 4 kHz  |

The Course Files are the four training WAVs called out in the Level 1 course
(Google Drive: Production/Courses/Ear Training (Level 1)/Training Files), gain-matched
from their masters. Piano is a 40 s excerpt (116–156 s) of Musopen's CC0 recording of
Chopin's Nocturne Op. 32 No. 1 (archive.org item `musopen-chopin`).

Planned additions (Level 3 program material, per the TET-3 syllabus — all run 125 Hz – 8 kHz):
speech English male (Kyle records; LibriVox speech rejected on quality), speech female +
speech German (source TBD), full mix (bounce of the stem song). The syllabus "classical
guitar" and "solo instrument" slots are covered by Acoustic Guitar / Acoustic and Piano.

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
