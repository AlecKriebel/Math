#!/bin/sh
set -eu
cd "$(dirname "$0")"
python independent_controls.py
python test_strict_validation.py
printf 'Independent review controls passed. Original target remains unsolved, exhausted 5/5.\n'
