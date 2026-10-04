#!/usr/bin/env python3
"""Verify the frozen public inventory; generated __pycache__ is ignored."""
import hashlib,json
from pathlib import Path
P=Path(__file__).parent
expected=json.loads((P/'SHA256SUMS.json').read_text())
actual={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in P.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert actual==expected, 'public file inventory or hashes differ from author freeze'
print(json.dumps({'matched_files':len(actual),'all_match':True}))
