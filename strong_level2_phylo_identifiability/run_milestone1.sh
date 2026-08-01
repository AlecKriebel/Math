#!/bin/sh
set -eu

PYTHONPATH=src .venv/bin/python src/verify_model_robustness.py
python3 src/verify_model_robustness_stdlib.py

