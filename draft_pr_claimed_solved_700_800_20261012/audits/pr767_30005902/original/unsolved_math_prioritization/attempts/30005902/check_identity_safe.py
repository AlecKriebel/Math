#!/usr/bin/env python3
"""Run the preserved optional identity checker with assertions always active."""
import sys
from pathlib import Path

def run_source(path, args):
    path = Path(path).resolve()
    old = sys.argv
    try:
        sys.argv = [str(path), *args]
        scope = {'__name__': '__main__', '__file__': str(path), '__package__': None}
        exec(compile(path.read_bytes(), str(path), 'exec', optimize=0), scope)
    finally:
        sys.argv = old

if __name__ == '__main__':
    run_source(Path(__file__).resolve().parent/'audit'/'check_identity.py', sys.argv[1:])
