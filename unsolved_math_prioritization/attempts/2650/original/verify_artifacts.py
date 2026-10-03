#!/usr/bin/env python3
"""Check this frozen package and replay its scoped finite computations."""
import hashlib,json,subprocess,sys
from pathlib import Path

base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
entries=manifest['files']
expected={e['path'] for e in entries}|{'MANIFEST.json'}
actual={p.name for p in base.iterdir() if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for e in entries:
    p=base/e['path']
    data=p.read_bytes()
    assert len(data)==e['bytes'],p.name
    assert hashlib.sha256(data).hexdigest()==e['sha256'],p.name
    assert p.suffix in {'.md','.json','.py'},p.name
status=json.loads((base/'status.json').read_text())
assert status['numeric_id']==2650
assert status['substantive_attempts']==status['budget']==5
assert status['research_status']=='exhausted'
assert status['mathematical_status']=='unresolved'
assert status['full_candidate'] is False
assert status['novelty_established'] is False
assert {p.name for p in base.glob('turn_*.md')}=={f'turn_{i:02}.md' for i in range(1,6)}
for script in ('chain_obstruction.py','power_commutator_frontier.py'):
    subprocess.run([sys.executable,str(base/script)],check=True,cwd=base)
# Deterministic results must remain identical after rerun.
for e in entries:
    assert hashlib.sha256((base/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
print(json.dumps({'id':2650,'manifest_files':len(entries),'attempts':5,
                  'mathematical_status':'unresolved','checks_passed':True,
                  'scope':'File integrity and finite arithmetic only; no independent proof audit.'}))
