#!/usr/bin/env python3
"""Check author-freeze bytes only; this is not a mathematical verifier."""
from pathlib import Path
import hashlib,json,sys
p=Path(__file__).resolve().parent
j=json.loads((p/'SHA256SUMS.json').read_text())
expected=set(j['files'])
actual={str(x.relative_to(p)) for x in p.rglob('*') if x.is_file() and x.name!='SHA256SUMS.json' and '__pycache__' not in x.parts}
errors=[]
if expected!=actual:errors.append({'missing':sorted(expected-actual),'extra':sorted(actual-expected)})
for n,record in j['files'].items():
    q=p/n
    if q.exists():
        b=q.read_bytes()
        if hashlib.sha256(b).hexdigest()!=record['sha256'] or len(b)!=record['bytes']:errors.append(n)
print(json.dumps({'result':'PASS' if not errors else 'FAIL','file_count':len(expected),'errors':errors,'limit':'File integrity only, not proof correctness.'},indent=2))
sys.exit(bool(errors))
