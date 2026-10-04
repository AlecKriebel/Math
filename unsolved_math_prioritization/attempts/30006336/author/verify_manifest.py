#!/usr/bin/env python3
"""Verify only the frozen author packet, without relying on source downloads."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert actual==set(manifest), (actual-set(manifest),set(manifest)-actual)
for name,expected in manifest.items():
    assert Path(name).name==name
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,name
status=json.loads((root/'STATUS.json').read_text())
assert status['status']=='unsolved'
assert status['attempt_turns']==5
assert not status['exact_resolution'] and not status['novelty_claim']
assert len((root/'turns.jsonl').read_text().splitlines())==5
assert json.loads((root/'CONTROL_RESULTS.json').read_text())['all_checks_pass']
assert all(p.suffix not in {'.pdf','.html','.sqlite'} for p in root.iterdir())
print(json.dumps({'manifest_valid':True,'files_checked':len(manifest),'status':'unsolved'}))
