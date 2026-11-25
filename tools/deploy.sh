#!/bin/sh
# Publishes the site: this folder is the repo github.com/amermdd2007-cell/portfolio, served by GitHub Pages
# at https://amermdd2007-cell.github.io/portfolio/ . Run from Git Bash after editing:  sh tools/deploy.sh
set -e
cd "$(dirname "$0")/.."
python tools/build_pages.py
git add -A
git commit -q -m "Update portfolio" || echo "nothing new to commit"
git push -q origin main
echo "Live in 1-2 minutes: https://amermdd2007-cell.github.io/portfolio/"
