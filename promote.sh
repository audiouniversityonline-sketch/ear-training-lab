#!/usr/bin/env bash
# promote.sh — publish the verified staging build to production.
#
# The iteration loop:
#   1. Edit and test staging.html (locally, and via the private staging URL).
#      Commit/push staging.html as often as you like — members never see it.
#   2. When it's good, ship it:
#        ./promote.sh "what changed"            # commit + push
#        ./promote.sh "what changed" v2.2       # ...and tag the release
#   3. This copies staging.html -> lab.html and pushes. GitHub Pages redeploys
#      the live members + free embeds in about a minute.
#
# Production (what Circle embeds):  lab.html        and  lab.html?free=1
# Staging   (private testing only): staging.html    and  staging.html?free=1
#
# If a promoted build turns out bad, roll back fast:
#   git revert HEAD && git push        (undo the last promote)
#   or re-promote a known-good tag.

set -euo pipefail

# Always operate from the repo root (the folder this script lives in),
# no matter where it's called from.
cd "$(dirname "$0")"

MSG="${1:-Promote staging build to production}"
TAG="${2:-}"

if [[ ! -f staging.html || ! -f lab.html ]]; then
  echo "✗ Couldn't find staging.html and lab.html here." >&2
  echo "  Run this from the ear-training-lab repo root." >&2
  exit 1
fi

# Copy the verified staging build over production.
cp staging.html lab.html

# Stage both so the repo stays consistent: the committed staging.html always
# matches the committed lab.html (i.e. matches what's live).
git add staging.html lab.html

if git diff --cached --quiet; then
  echo "✓ Nothing to promote — production already matches staging."
  exit 0
fi

git commit -q -m "$MSG"
echo "✓ Committed: $MSG"

git push -q origin main
echo "✓ Pushed to main (Pages will redeploy in ~1 min)."

if [[ -n "$TAG" ]]; then
  git tag "$TAG"
  git push -q origin "$TAG"
  echo "✓ Tagged $TAG and pushed the tag."
fi

echo ""
echo "Live shortly at:"
echo "  Members: https://audiouniversityonline-sketch.github.io/ear-training-lab/lab.html"
echo "  Free:    https://audiouniversityonline-sketch.github.io/ear-training-lab/lab.html?free=1"
