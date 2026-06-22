# Ear Training Lab

An interactive EQ ear-training tool for [Audio University](https://www.youtube.com/@AudioUniversity). Single-page apps, no build step (React + Babel via CDN). Learners train their ears to identify frequency boosts and cuts across a 15-week curriculum. The free sample is the lead magnet; the full course is for members.

## Files

- **`index.html`** — the **free** lead-magnet app, served at the site root. Loads `curriculum-free.json`.
- **`full.html`** — the **paid** app: full 15-week Level 1 curriculum, manual practice, multi-filter rounds. Loads `curriculum.json`.
- **`curriculum.json` / `curriculum-free.json`** — the task curricula. **These are the files to edit when changing or adding tasks.** Schema: `{ schemaVersion, levels: [...], lockedLevels: [...] }`. Each app has an inline fallback if the fetch fails.
- **`sources/`** — optional curated WAV library for the full app's Source Material picker (drop in WAVs named per `sources/README.md`). The default pink-noise source and custom uploads work without these.
- **`design-system.css`** — the canonical Audio University interactive-tool design tokens + component recipes, shared across the training-tool suite. The apps stay self-contained and copy from this; treat it as the source of truth.
- **`HANDOFF.md`** — full project state and history for a fresh session.

## Hosting

Served via GitHub Pages and embedded in an iframe on the Audio University Circle community. The member page (full app) is gated to an access group; the free page is open as a lead magnet.

- Free app: `https://audiouniversityonline-sketch.github.io/ear-training-lab/`
- Full app: `https://audiouniversityonline-sketch.github.io/ear-training-lab/full.html`

A commit to `main` auto-deploys to the live Pages URL within about a minute. That is the whole content pipeline: edit a curriculum file (or the app), commit, and it is live.

> **Note:** `lab.html` is the current unified app (EQ + Compression in one file) and is what the Circle pages embed today — members at `lab.html`, free visitors at `lab.html?free=1`. The standalone `index.html` / `full.html` above are the earlier EQ-only apps.

## Developing safely (staging → production)

Because Pages deploys from `main`, **anything pushed to `main` is live immediately.** To iterate without risking the live experience, work on a staging copy and promote only when it's verified.

- **`lab.html` = production.** What Circle embeds. Don't hand-edit it — let `promote.sh` update it.
- **`staging.html` = your sandbox.** Edit and push this as often as you like. It has a public URL but nothing links to it, so the public never sees it.

**The loop:**

1. **Edit `staging.html`** and test it locally (open the file directly, or `python3 -m http.server` then visit `staging.html`). The app is a single file with no build step, so local behavior matches production exactly.
2. **Test it like it's real (optional but recommended):** commit/push, then embed the private staging URL in a *hidden* Circle page (a draft, or an admin-only space) to try it inside the real iframe and on real devices:
   - Members view: `https://audiouniversityonline-sketch.github.io/ear-training-lab/staging.html`
   - Free view: `https://audiouniversityonline-sketch.github.io/ear-training-lab/staging.html?free=1`
3. **Promote when happy:**
   ```sh
   ./promote.sh "what changed"          # copy staging → production, commit, push
   ./promote.sh "what changed" v2.2     # ...and tag the release
   ```
   Live in about a minute.
4. **Roll back if needed:** `git revert HEAD && git push` undoes the last promote in ~1 minute. Any tagged version is also restorable from the Releases page.

**One gotcha:** browser `localStorage` is scoped to the origin (`github.io`), not the file path, so `staging.html` and `lab.html` share saved progress on *your own* browser. For copy/UI/audio changes this never matters. Only when testing a change to the **storage schema or keys**, use a private/incognito window so you don't scramble your own production progress. (Other members are never affected — they don't visit staging.)

When juggling two files starts to feel limiting, the upgrade is **Cloudflare Pages** pointed at this repo: production from `main`, plus an automatic private preview URL for every branch/PR, on a separate origin (which also isolates `localStorage`). It requires changing the Circle iframe URL once, so hold off until the two-file flow feels limiting.

## Progress

Learner progress is saved in the browser via `localStorage`, keyed by each level's stable `id` (storage schema v2, auto-migrates legacy v1). Keep `id`s stable and append new content rather than renumbering, so content updates never reset a learner's progress.

## Audio

Default training audio is pink noise synthesized in the browser with the Web Audio API — nothing to load. The full app can also EQ-train against custom WAV uploads or the curated `sources/` library. Sound starts off and resumes on the first interaction (browser autoplay policy).

## Versioning

Releases are tagged on GitHub; any prior version is restorable from the Releases page.

- **`v1.0-light`** — the original light "paper & ink" theme.
- **`v2.0-dark`** — the dark "pro-console" theme matching the Troubleshooting Lab, plus a live EQ-curve display, streak + accuracy meter, and richer answer feedback.
- **`v2.1`** — responsive three-zone "bench" layout: a persistent course/progress rail, a center training stage, and an always-visible session HUD on desktop; on mobile the same zones stack and the transport docks to a fixed bottom bar in the thumb zone. No audio/scoring/curriculum changes (current).
