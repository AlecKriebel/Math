#!/bin/sh
set -eu

./run_milestone1.sh
PYTHONPATH=src python3 src/verify_generator_atlas.py
PYTHONPATH=src .venv/bin/python src/verify_jc_four_network_class.py
PYTHONPATH=src python3 src/verify_jc_four_network_class_stdlib.py
