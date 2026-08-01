#!/bin/sh
set -eu

./run_milestone1.sh
PYTHONPATH=src python3 src/verify_generator_atlas.py

