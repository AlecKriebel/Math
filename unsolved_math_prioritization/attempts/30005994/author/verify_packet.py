#!/usr/bin/env python3
"""Verify frozen membership and replay the exact mathematical controls."""
import hashlib,json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
expected=set(m['files'])|{'AUTHOR_MANIFEST.json'}
actual={p.name for p in root.iterdir() if p.is_file()}
if actual!=expected:
    raise RuntimeError('Unexpected packet membership: '+str(actual^expected))
for name,entry in m['files'].items():
    b=(root/name).read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise RuntimeError('Byte/hash mismatch: '+name)
record=json.loads((root/'EXACT_RESULTS.json').read_text())
with tempfile.TemporaryDirectory(prefix='gradient-check-') as cwd:
    for optimized in [False,True]:
        args=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/'verify_exact.py')]
        proc=subprocess.run(args,cwd=cwd,text=True,capture_output=True,check=True)
        if json.loads(proc.stdout)!=record:
            raise RuntimeError('Replay differs: optimized='+str(optimized))
print(json.dumps({'result':'PASS','payload_files':len(m['files']),'mathematical_checks_per_replay':record['checks'],'normal_replay':True,'optimized_replay':True,'different_cwd':True,'claim':'Partial results only; original general-potential question remains unsolved.'},indent=2,sort_keys=True))
