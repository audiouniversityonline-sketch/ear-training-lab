#!/usr/bin/env python3
"""
Build production lab.html from staging.html.

staging.html stays authored as JSX (edit it exactly as before). This compiles that
JSX ahead of time so the shipped page does NOT download Babel (~3MB) or spend
seconds compiling ~380KB of JSX in the browser on every visit. That compile step
was leaving members looking at an empty dark page while they waited.

It also removes every other third-party dependency from the shipped page:
  - Tailwind is compiled to a static stylesheet (the CDN build is ~400KB of JS that
    generates CSS in the browser on every load) and inlined.
  - React and ReactDOM are inlined from vendor/ (pinned copies in this repo).
  - Fonts are served from fonts/ (handled in staging.html itself).
The build fails if any third-party script or stylesheet survives in lab.html.
"""
import re, subprocess, sys, os, tempfile

SRC, OUT = "staging.html", "lab.html"
ESBUILD = ["npx", "--yes", "esbuild@0.21.5"]
TAILWIND = ["npx", "--yes", "tailwindcss@3.4.17"]  # same version staging loads from the CDN

def fail(msg):
    print("BUILD FAILED: " + msg, file=sys.stderr)
    sys.exit(1)

html = open(SRC, encoding="utf-8").read()

m = re.search(r'(<script type="text/babel"[^>]*>)(.*?)(</script>)', html, re.S)
if not m:
    fail("could not find the text/babel block in " + SRC)
jsx = m.group(2)

with tempfile.TemporaryDirectory() as tmp:
    src_path = os.path.join(tmp, "app.jsx")
    open(src_path, "w", encoding="utf-8").write(jsx)
    try:
        r = subprocess.run(
            ESBUILD + [src_path, "--target=es2015", "--format=iife",
                       "--log-level=warning"],
            capture_output=True, text=True)
    except FileNotFoundError:
        fail("npx not found; Node is required to build")
    if r.returncode != 0:
        fail("esbuild error:\n" + (r.stderr or r.stdout))
    compiled = r.stdout

if not compiled.strip():
    fail("esbuild produced no output")

# A literal </script> inside the JS would end the tag early.
compiled = compiled.replace("</script", "<\\/script")

out = html[:m.start()] + "<script>\n" + compiled + "\n  </script>" + html[m.end():]

# Babel is no longer needed at runtime; drop its CDN script and its fallback.
before = out
out = re.sub(r'[ \t]*<script src="https://unpkg\.com/@babel/standalone@7/babel\.min\.js"></script>\n', "", out)
out = re.sub(r'[ \t]*<script>window\.Babel\|\|document\.write\([^\n]*\n', "", out)
if out == before:
    fail("expected to remove the Babel script tags but found none")
if "babel" in out.lower().split("<body")[0]:
    fail("a Babel reference survived in the head")

# --- Tailwind: compile the utilities staging.html actually uses -----------------
cfg = re.search(r'[ \t]*<script>\s*tailwind\.config = (\{.*?\n    \});\s*</script>\n', out, re.S)
if not cfg:
    fail("could not find the tailwind.config block")
with tempfile.TemporaryDirectory() as tmp:
    open(os.path.join(tmp, "tailwind.config.js"), "w", encoding="utf-8").write(
        "const c = " + cfg.group(1) + ";\nc.content = [%r];\nmodule.exports = c;\n" % os.path.abspath(SRC))
    open(os.path.join(tmp, "in.css"), "w").write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
    r = subprocess.run(TAILWIND + ["-c", os.path.join(tmp, "tailwind.config.js"),
                                   "-i", os.path.join(tmp, "in.css"), "--minify"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        fail("tailwind error:\n" + r.stderr)
    tw_css = r.stdout.strip()
out = out[:cfg.start()] + out[cfg.end():]
n_before = len(out)
out = re.sub(r'[ \t]*<script src="https://cdn\.tailwindcss\.com[^"]*"></script>\n', "", out)
if len(out) == n_before:
    fail("expected to remove the Tailwind CDN script but found none")
# The CDN build appends its stylesheet to the end of <head>, after the app's own
# <style>. Same position here so the cascade is unchanged.
out = out.replace("</head>", "<style>" + tw_css + "</style>\n</head>", 1)

# --- React: inline the pinned copies from vendor/ ------------------------------
def inline_vendor(mm):
    js = open(mm.group(1), encoding="utf-8").read().replace("</script", "<\\/script")
    return "<script>" + js + "</script>"
out, n = re.subn(r'<script src="(vendor/[^"]+)"></script>', lambda mm: inline_vendor(mm), out)
if n != 2:
    fail("expected to inline 2 vendor scripts (React, ReactDOM), found %d" % n)

# --- Guard: nothing may load from a third party ---------------------------------
third = re.findall(r'<(?:script|link)\b[^>]*\b(?:src|href)="(https?://[^"]+)"', out)
third += re.findall(r'document\.write\([^)]*https?://[^)]*\)', out)
if third:
    fail("third-party resources survived in the build:\n  " + "\n  ".join(third))

open(OUT, "w", encoding="utf-8").write(out)

print("built %s from %s" % (OUT, SRC))
print("  JSX %.0f KB -> %.0f KB of plain JS; Tailwind -> %.0f KB of static CSS; React inlined"
      % (len(jsx)/1024, len(compiled)/1024, len(tw_css)/1024))
print("  page: %.0f KB, no third-party scripts, styles or fonts" % (len(out)/1024))
