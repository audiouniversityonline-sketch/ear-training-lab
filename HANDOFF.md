# Ear Training Lab — Project Handoff

This file captures the current state of the project so a fresh Claude Code session can pick up without re-reading thousands of lines. The full design rationale is in the plan file at `~/.claude/plans/the-basic-functionality-of-stateless-aho.md`.

## Project files

```
ear-training-lab/  (GitHub: audiouniversityonline-sketch/ear-training-lab → GitHub Pages)
├── index.html                       (free lead-magnet app — served at the site root)
├── full.html                        (paid app — full 15-week curriculum, multi-filter)
├── curriculum.json                  (Level 1: 15 weeks of tasks; full version)
├── curriculum-free.json             (3 sample tasks + locked-level tease metadata)
├── sources/                         (curated source-material WAV library; see its README)
│   └── README.md
├── design-system.css                (shared AU interactive-tool tokens + component recipes)
├── README.md                        (repo overview + the push-to-deploy pipeline)
└── HANDOFF.md                       (this file)
```

Both HTML files are single-file React apps loaded via Babel-standalone. No build step.

## What's shipped (per phase from the plan)

| Phase | Status | What it does |
|---|---|---|
| **1a — JSON curriculum loader** | ✅ shipped (both) | Curriculum lives in `curriculum.json` / `curriculum-free.json`. Schema: `{ schemaVersion, levels: [...], lockedLevels: [...] }`. Inline fallback if fetch fails |
| **1b — Multi-level picker + per-level progress** | ✅ shipped (both) | `CurriculumPicker` has a level switcher. Progress storage v2: `{ schemaVersion: 2, levels: { [id]: { [week]: { [taskIdx]: {completed, score} } } } }`. Auto-migrates legacy v1 |
| **1c — Third-octave helpers** | ✅ shipped (both) | `octaveOf(freq)` and `groupByOctave(bands)` available. Engine already supported thirds via `freqSet` |
| **1d — Direction-as-test** | ✅ shipped (both) | `direction: "auto"` and `"mixed"` aliases. Engine already had this — just aliased |
| **1e (deferred) → Phase 6** | ✅ shipped (full only) | See Phase 6 below |
| **1f — Keyboard shortcuts + cheat sheet** | ✅ shipped (both) | `1`–`9` octave bands, `,`/`.` thirds nudge, `↑`/`↓` direction, `A`/`B`/`C` channels, Space play/pause, Enter submit, `N`/`→` next, `R` replay, `?` cheat sheet, `Esc` close |
| **2a — Manual mode** | ✅ shipped (full only) | `<ManualSetup>` panel. Inputs: mode, resolution (oct/thirds), direction, gain, rounds, timer, frequencies, **filterCount, gainOptions** (added in Phase 6). Persisted to localStorage |
| **2b — Lock 3 modes in free** | ✅ shipped (free) | Identify, RTF, RTF Memory show with lock icon, route to membership URL on click |
| **2c — Manual mode tease in free** | ✅ shipped (free) | Locked Manual Practice card in free curriculum picker |
| **3a — Mistake review** | ✅ shipped (both) | A/B between actual filter and user's guess on Channel B. Single-filter rounds only — multi-filter rounds use the per-slot ✓/✗ reveal instead |
| **3b — Learn mode** | ✅ shipped (both) | Practice/Learn toggle in header. In Learn: pick freq, see label, toggle boost/cut, no scoring |
| **5a — Curated source library** | ✅ shipped (full) | `SOURCE_LIBRARY` constant + `loadSourceFromLibrary` + Source Material section in settings drawer. WAVs go in `/sources/`. Locked tease in free's settings drawer |
| **5b — Shareable result card** | ✅ shipped (free) | `buildShareCardBlob` draws 1080×1080 PNG via canvas. `shareResultCard` uses Web Share API with download fallback. Wired into TaskCompleteModal |
| **6 — Multi-filter rounds with variable gain** | ✅ shipped (full only) | See below |

## Phase 6 — Multi-filter (most recent ship, full v2 only)

**Schema additions to task struct (both optional, defaults preserve single-filter behavior):**
- `filterCount: 1 | 2 | 3` — how many simultaneous filters per round
- `gainOptions: [number, ...]` — pool of allowed gain magnitudes; engine picks one per filter per round

**Engine architecture:**
- `MAX_FILTERS = 3` constant
- `filtersRef.current.questions / questionsForC / answers` are arrays of 3 peaking BiquadFilters wired in series per chain
- Unused slots stay at 0 dB gain (peaking-at-0 is bit-identical to passthrough — preserves single-filter behavior)
- Helpers: `bypassChain()`, `applyFilterSlot()`

**State:**
- `filterCount`, `gainOptions` (per-task)
- `guessFilters: [{freq, direction, gainDb}, ...]` and `answerFilters: [...]` for multi-filter
- For single-filter rounds, `round.freq/direction/gainDb` legacy scalars are still populated

**Round shape:**
```js
// Single-filter (existing curriculum):
round = {
  filters: [{ freq: 1000, direction: "boost", gainDb: 12 }],
  freq: 1000, direction: "boost", gainDb: 12   // legacy scalars for back-compat
}

// Multi-filter:
round = {
  filters: [
    { freq: 125,  direction: "cut",   gainDb: 12 },
    { freq: 1000, direction: "boost", gainDb: 6  },
    { freq: 4000, direction: "boost", gainDb: 12 }
  ]
  // legacy scalars intentionally absent
}
```

**Scoring:** binary set-match via `evaluateMultiFilter()`. Every user filter must match some actual filter on `(freq, direction, gainDb)` — order doesn't matter. RTF inverts the direction.

**UI:** when `filterCount > 1` OR `gainOptions.length > 1`, the slot-based picker activates: one card per filter slot with freq pills + (optional) direction toggle + (optional) gain picker. Distinct freqs enforced. Submit gated until every slot is fully populated.

## How to author a new task

Edit `curriculum.json`. Single-filter (current Level 1 style):
```json
{ "name": "Matching mids +12", "mode": "Matching", "freqSet": "mids_octaves",
  "bandwidth": "1.0_oct", "gainDb": 12, "direction": "boost", "rounds": 25 }
```

Multi-filter with mixed gains (Phase 6):
```json
{ "name": "L2-W3 — Three filters mixed", "mode": "Matching", "freqSet": "full_octaves",
  "filterCount": 3, "gainOptions": [6, 12], "direction": "auto", "rounds": 20 }
```

Available `freqSet` values (from `FREQ_SETS` in both HTML files):
- Octaves: `mids_octaves`, `full_octaves`, `low_mids`, `high_mids`, `lows_octaves`, `highs_octaves`, `octaves_125_8k`
- Thirds: `mids_thirds`, `full_thirds`, `thirds_125_500`

To add new freqSets, edit the `FREQ_SETS` constant in both HTML files (one place each).

## Deferred / not shipped

- **Multi-filter mistake review** — single-filter mistake review works; for multi-filter, the per-slot ✓/✗ reveal serves the same purpose for now
- **Slot-aware keyboard shortcuts** — `Tab` to cycle slots, `[`/`]` to cycle gain. Mouse-driven slot picker works fully
- **Phase 4 — Circle integration** — achievements endpoint, member identification, event firing, course-lesson mapping. Requires a backend endpoint (planned: Cloudflare Worker)
- **Phase 1e (audio engine multi-filter graph)** — superseded by Phase 6 which did this work
- **Email capture in free version** — explicitly skipped per user
- **Weighted/spaced sampling** — explicitly skipped per user
- **Refactor to single engine + two configs** — both files are diverging more, but not blocking

## Three high-leverage ideas brainstormed (all deferred)

1. **Per-band mastery profile + adaptive sampling** — pedagogy lever; track per-band accuracy, weight sampling toward weak spots, build "Your Ear Map" view
2. **Daily Challenge with streak (free version)** — Wordle-style daily hook with shareable result card
3. **UTM-tagged conversion CTAs + Plausible analytics** — funnel measurement for the conversion surfaces we shipped

## Critical decision pending: deploy infrastructure migration

Currently: Google Drive (source) → manual FTP upload → website host → iframe in Circle.

Recommended: GitHub repo (source) → Cloudflare Pages (auto-deploy on push) → custom subdomain → iframe in Circle (URL change only).

**Why before Phase 4:** Phase 4 needs a backend endpoint for the Circle achievements API. Cloudflare Pages includes Workers (serverless functions) on the same deploy. Setting this up first means Phase 4 is mostly "add a function file to the repo."

**Migration time:** ~1 hour for setup + ~30 min to verify the Circle iframe still works.

## Recommended next session priorities

1. **Walk through the GitHub + Cloudflare Pages migration** with the user. Verify the Circle iframe works on the new subdomain.
2. **Phase 4 — Circle integration:**
   - 4a: Cloudflare Worker handler for `/achievements` (uses Circle API token from env secret)
   - 4b: "Connect to Audio University" section in Settings drawer (email-based identification)
   - 4c: Achievement events: task complete, week complete, level complete, streak milestones
   - 4d: Course-lesson mapping: query existing 15 lessons, populate `circleLessonId` field on each week in `curriculum.json`
3. **Optional:** wire up Plausible Analytics + UTM-tagged CTAs while we're touching the deploy.

## Notes on code conventions

- React via CDN + Babel-standalone (no build step). Both files use `<script type="text/babel" data-presets="env,react">`
- Tailwind via CDN
- localStorage helpers via `STORAGE.get(key, default)` / `STORAGE.set(key, value)`
- Only emojis used in code: `↑` `↓` `←` `→` `✓` `✗` (display only). User explicitly requested no emoji additions
- Membership URL constant: `MEMBERSHIP_URL = "https://audiouniversityonline.com/membership"` — used by all locked-feature CTAs

## User context

- Kyle Mathias runs Audio University (15-week ear training course on Circle)
- Brand voice: monochrome paper/ink design with red accent (`#e63946`), Poppins italic for display, JetBrains Mono for stats
- Free version is a lead magnet for the paid course
- 15-week curriculum corresponds 1:1 with 15 lessons in an existing Circle course (mapping wired in Phase 4d)
