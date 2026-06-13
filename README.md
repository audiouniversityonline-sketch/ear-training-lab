# Ear Training Lab

An interactive EQ ear-training tool for [Audio University](https://www.youtube.com/@AudioUniversity). Single-page apps, no build step (React + Babel via CDN). Learners train their ears to identify frequency boosts and cuts across a 15-week curriculum. The free sample is the lead magnet; the full course is for members.

## Files

- **`index.html`** — the **free** lead-magnet app, served at the site root. Loads `curriculum-free.json`.
- **`full.html`** — the **paid** app: full 15-week Level 1 curriculum, manual practice, multi-filter rounds. Loads `curriculum.json`.
- **`curriculum.json` / `curriculum-free.json`** — the task curricula. **These are the files to edit when changing or adding tasks.** Schema: `{ schemaVersion, levels: [...], lockedLevels: [...] }`. Each app has an inline fallback if the fetch fails.
- **`sources/`** — optional curated WAV library for the full app's Source Material picker (drop in WAVs named per `sources/README.md`). The default pink-noise source and custom uploads work without these.
- **`HANDOFF.md`** — full project state and history for a fresh session.

## Hosting

Served via GitHub Pages and embedded in an iframe on the Audio University Circle community. The member page (full app) is gated to an access group; the free page is open as a lead magnet.

- Free app: `https://audiouniversityonline-sketch.github.io/ear-training-lab/`
- Full app: `https://audiouniversityonline-sketch.github.io/ear-training-lab/full.html`

A commit to `main` auto-deploys to the live Pages URL within about a minute. That is the whole content pipeline: edit a curriculum file (or the app), commit, and it is live.

## Progress

Learner progress is saved in the browser via `localStorage`, keyed by each level's stable `id` (storage schema v2, auto-migrates legacy v1). Keep `id`s stable and append new content rather than renumbering, so content updates never reset a learner's progress.

## Audio

Default training audio is pink noise synthesized in the browser with the Web Audio API — nothing to load. The full app can also EQ-train against custom WAV uploads or the curated `sources/` library. Sound starts off and resumes on the first interaction (browser autoplay policy).

## Versioning

Releases are tagged on GitHub; any prior version is restorable from the Releases page.

- **`v1.0-light`** — the original light "paper & ink" theme.
