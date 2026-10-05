#!/usr/bin/env python3
"""Root actual entrypoint for the completely read, pinned private collector."""
from pathlib import Path
import hashlib, runpy, sys
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent
C=A/'root_replay_preparation_family/collect_root_replays.py'
assert sys.flags.optimize==0
assert hashlib.sha256(C.read_bytes()).hexdigest()=='a1bfc3d7cb873acb24343b2a70a6bd5bf63466ba343fae157dcc91e0d65147a5'
sys.argv=[str(C),'--root-script-path',str(Path(__file__).resolve()),*sys.argv[1:]]
runpy.run_path(str(C),run_name='__main__')
