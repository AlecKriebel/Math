#!/usr/bin/env python3
"""Root-owned explicit entrypoint for the completely reviewed closed PR38 collector."""
import hashlib
from pathlib import Path
import runpy
import sys
sys.dont_write_bytecode = True
assert not sys.flags.optimize
A = Path(__file__).resolve().parent
assert A.name == 'pr38_2765' and A.parents[2] == Path('/Users/alec/Documents/Math')
source = A / 'root_replay_execution_revision/collect_root_replays.py'
assert source.is_file() and not source.is_symlink()
assert hashlib.sha256(source.read_bytes()).hexdigest() == '523e9daa992a7eb8047e5736d98ff2361102d427086ae5a7d26ee028cec3a9c4'
sys.argv = [str(source), *sys.argv[1:]]
runpy.run_path(str(source), run_name='__main__')
