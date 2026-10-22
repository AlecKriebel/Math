#!/usr/bin/env python3
"""Verify this source-free frozen packet and rerun its deterministic math checks."""
from pathlib import Path
import hashlib,json,subprocess,sys
def require(condition, message):
    """Retain validation in normal, -O, and -OO interpreters."""
    if not condition:
        raise ValueError(message)

base=Path(__file__).resolve().parent
manifest=json.loads((base/'FROZEN_MANIFEST.json').read_text())
expected={item['path']:item for item in manifest['files']}
actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and p.name!='FROZEN_MANIFEST.json'}
require(actual==set(expected), (actual-set(expected),set(expected)-actual))
for name,item in expected.items():
    data=(base/name).read_bytes()
    require(len(data)==item['bytes'], name)
    require(hashlib.sha256(data).hexdigest()==item['sha256'], name)
require(all(Path(name).suffix in {'.md','.py','.json'} for name in expected), 'verify_packet.py:14: verification predicate failed')
observed=json.loads(subprocess.check_output([sys.executable,str(base/'check_math.py')],text=True))
saved=json.loads((base/'CHECK_RESULTS.json').read_text())
require(observed==saved, 'verify_packet.py:17: verification predicate failed')
require(observed['status']=='PASS' and observed['does_not_prove_original_problem'], 'verify_packet.py:18: verification predicate failed')
print(json.dumps({'status':'PASS','verified_files':len(expected),'math_results_reproduced':True,'problem_status':'unresolved'},sort_keys=True))
