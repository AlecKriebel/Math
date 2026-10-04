#!/usr/bin/env python3
"""Root actual entrypoint for the completely read, pinned private collector."""
from pathlib import Path
import hashlib, runpy, sys
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent
C=A/'root_replay_execution_revision/collect_root_replays.py'
assert sys.flags.optimize==0
assert hashlib.sha256(C.read_bytes()).hexdigest()=='9cfeaa5d0bcfda4f659e0b9746a66fc4a9519f29fd8afcc01709630e6d9f3299'
sys.argv=[str(C),'--root-script-path',str(Path(__file__).resolve()),*sys.argv[1:]]
runpy.run_path(str(C),run_name='__main__')
