#!/usr/bin/env python3
"""Root actual entrypoint for the completely read, pinned private collector."""
from pathlib import Path
import hashlib, runpy, sys
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent
C=A/'root_replay_execution_revision/collect_root_replays.py'
assert sys.flags.optimize==0
assert hashlib.sha256(C.read_bytes()).hexdigest()=='c99cb88952cdd464f7c86ce0ea1736bf7b2d643ce7f0b07ad41d41bb873df0a3'
sys.argv=[str(C),'--root-script-path',str(Path(__file__).resolve()),*sys.argv[1:]]
runpy.run_path(str(C),run_name='__main__')
