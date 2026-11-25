#!/bin/sh
# Publishes the committed site to https://amermdd2007-cell.github.io/portfolio/
# (a folder inside the amermdd2007-cell.github.io repo; the Bug Hunter page and app-ads.txt at its root stay as they are).
# Run from Git Bash after committing here:  sh tools/deploy.sh
set -e
SITE="$(cd "$(dirname "$0")/.." && pwd)"
PAGES="$HOME/Desktop/amermdd2007-cell.github.io"
git -C "$PAGES" pull -q --ff-only
rm -rf "$PAGES/portfolio"
mkdir -p "$PAGES/portfolio"
git -C "$SITE" archive HEAD | tar -x -C "$PAGES/portfolio"
rm -rf "$PAGES/portfolio/tools" "$PAGES/portfolio/.gitignore"
git -C "$PAGES" add -A portfolio
git -C "$PAGES" commit -q -m "Update portfolio" && git -C "$PAGES" push -q origin HEAD || echo "nothing changed"
echo "Live in 1-2 minutes: https://amermdd2007-cell.github.io/portfolio/"
