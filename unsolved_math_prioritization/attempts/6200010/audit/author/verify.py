#!/usr/bin/env python3
"""Verify the frozen authored inventory and replay deterministic finite controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

def fail(message):
    raise RuntimeError(message)

def main():
    root=Path(__file__).resolve().parent
    manifest_path=root/'MANIFEST.json'
    manifest=json.loads(manifest_path.read_text())
    if manifest.get('schema')!='math-author-freeze-v1' or manifest.get('problem_id')!=6200010:
        fail('wrong manifest identity')
    entries=manifest.get('files')
    if not isinstance(entries,list) or not entries: fail('empty or malformed inventory')
    wanted={}
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)!={'path','bytes','sha256'}:
            fail('malformed entry')
        name=entry['path'];p=Path(name)
        if not isinstance(name,str) or p.is_absolute() or '..' in p.parts or name=='MANIFEST.json':
            fail('unsafe path')
        if name in wanted: fail('duplicate path')
        if type(entry['bytes']) is not int or entry['bytes']<0: fail('invalid size')
        digest=entry['sha256']
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            fail('invalid digest')
        wanted[name]=entry
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink(): fail('symlink in frozen payload')
        if p.is_file() and p.name!='MANIFEST.json': actual.add(p.relative_to(root).as_posix())
    if actual!=set(wanted): fail('inventory mismatch')
    for name,entry in wanted.items():
        b=(root/name).read_bytes()
        if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
            fail('hash or size mismatch: '+name)
    identity=json.loads((root/'IDENTITY.json').read_text())
    if identity.get('problem_id')!=6200010 or identity.get('review_hash')!='a7ba968e284b4b4b467dcb2029da7bc249bc87135f05c936fadf91551909160d':
        fail('problem identity changed')
    if identity.get('disposition')!='partial_unresolved' or identity.get('turns_used')!=5:
        fail('unexpected author disposition')
    cmd=[sys.executable]
    if sys.flags.optimize: cmd.append('-O')
    cmd.append(str(root/'check_math.py'))
    proc=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    if proc.returncode: fail('calculation failed: '+proc.stderr)
    output=json.loads(proc.stdout)
    expected=json.loads((root/'CHECK_RESULTS.json').read_text())
    if output!=expected: fail('replay differs from frozen result')
    if output.get('checks')!=32400 or output.get('status')!='finite_controls_pass': fail('wrong check total/status')
    print(json.dumps({'status':'PASS','problem_id':6200010,'files_verified':len(wanted),
                      'finite_checks':output['checks'],'optimized':bool(sys.flags.optimize),
                      'original_problem':'unresolved','general_proof_formalized':False},sort_keys=True))

if __name__=='__main__':
    try: main()
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr)
        sys.exit(1)
