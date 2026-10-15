#!/usr/bin/env python3
"""Verify portable audit bindings; optionally bind and replay frozen author inputs."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,zipfile
p=argparse.ArgumentParser();p.add_argument('--author-root',type=Path);p.add_argument('--replay',action='store_true');args=p.parse_args()
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
def verify(path,rec):
    raw=path.read_bytes()
    assert len(raw)==rec['bytes'],f'Byte count mismatch: {path.name}'
    assert hashlib.sha256(raw).hexdigest()==rec['sha256'],f'Hash mismatch: {path.name}'
    return raw
for rec in manifest['audit_files']:verify(root/rec['path'],rec)
result={'audit_bindings':'pass','audit_payload_files':len(manifest['audit_files'])}
if args.author_root:
    a=args.author_root
    for name in ('AUTHOR_FREEZE.json','author-packet.zip'):verify(a/name,manifest['author_bindings'][name])
    freeze=json.loads((a/'AUTHOR_FREEZE.json').read_text())
    with zipfile.ZipFile(a/'author-packet.zip') as z:
        assert z.read('AUTHOR_FREEZE.json')==(a/'AUTHOR_FREEZE.json').read_bytes()
        for rec in freeze['files']:
            raw=verify(a/'packet'/rec['path'],rec)
            assert z.read('packet/'+rec['path'])==raw
    result['author_bindings']='pass';result['author_payload_files']=len(freeze['files'])
if args.replay:
    if not args.author_root:p.error('--replay requires --author-root')
    for script,expected in [('verify.py','REPLAY_CONTROL_RESULTS.json'),('verify_symbolic.py','REPLAY_SYMBOLIC_RESULTS.json')]:
        r=subprocess.run([sys.executable,str(args.author_root/'packet'/script)],capture_output=True,check=True)
        assert r.stdout==(root/expected).read_bytes(),f'Replay mismatch: {script}'
    r=subprocess.run([sys.executable,str(root/'independent_checks.py')],capture_output=True,check=True)
    new=json.loads(r.stdout);old=json.loads((root/'INDEPENDENT_RESULTS.json').read_text())
    # Runtime version strings are metadata, not mathematical certificate fields.
    versions={k:new.pop(k) for k in ['python','sympy']}
    for k in versions:old.pop(k)
    assert new==old,'Independent replay mismatch'
    result['author_replays']='byte-identical';result['independent_replay']='certificate-identical';result['runtime']=versions
print(json.dumps(result,indent=2))
