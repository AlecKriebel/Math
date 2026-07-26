#!/bin/sh
set -eu

python verify_certificate.py
python -m unittest discover -s tests -v
tectonic main.tex --outdir build

test -s build/main.pdf
printf '%s\n' "PASS: analytic artifacts built and finite verification checks passed."
