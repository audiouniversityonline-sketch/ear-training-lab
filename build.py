#!/usr/bin/env python3
"""
Build production lab.html from staging.html.

staging.html stays authored as JSX (edit it exactly as before). This compiles that
JSX ahead of time so the shipped page does NOT download Babel (~3MB) or spend
seconds compiling ~380KB of JSX in the browser on every visit. That compile step
was leaving members looking at an empty dark page while they waited.

React and ReactDOM still come from the CDN (with the jsdelivr fallback); only the
Babel dependency and the runtime transform are removed.
"""
import re, subprocess, sys, os, tempfile

SRC, OUT = "staging.html", "lab.html"
ESBUILD = ["npx", "--yes", "esbuild@0.21.5"]

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

open(OUT, "w", encoding="utf-8").write(out)

src_kb, out_kb = len(html) / 1024, len(out) / 1024
print("built %s from %s" % (OUT, SRC))
print("  compiled JSX: %.0f KB -> %.0f KB of plain JS" % (len(jsx)/1024, len(compiled)/1024))
print("  page: %.0f KB -> %.0f KB (Babel download of ~3 MB removed)" % (src_kb, out_kb))
