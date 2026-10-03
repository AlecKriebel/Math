#!/usr/bin/env python3
"""Root-owned explicit entrypoint for the completely reviewed closed PR39 collector."""
import hashlib
from pathlib import Path
import runpy
import sys
sys.dont_write_bytecode = True
assert not sys.flags.optimize
A = Path(__file__).resolve().parent
assert A.name == 'pr39_9500008' and A.parents[2] == Path('/Users/alec/Documents/Math')
source = A / 'root_replay_preparation_family/collect_root_replays.py'
assert source.is_file() and not source.is_symlink()
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'e414341700fed9539e56b5937a3457130411084348ed47d584602b558d105205'
sys.argv = [str(source), *sys.argv[1:]]
runpy.run_path(str(source), run_name='__main__')
