#!/usr/bin/env python3
"""Closed-inventory and exact offline replay verifier."""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent

def fail(msg): raise RuntimeError(msg)
manifest=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
expected=set(manifest['files'])|{'AUTHOR_MANIFEST.json'}
actual=set()
for p in ROOT.rglob('*'):
    if p.is_symlink(): fail('symlink member: '+p.name)
    if p.is_file():actual.add(p.relative_to(ROOT).as_posix())
if actual!=expected:fail('inventory differs: '+repr(sorted(actual^expected)))
for name,m in manifest['files'].items():
    p=pathlib.PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts:fail('unsafe path')
    data=(ROOT/name).read_bytes()
    if len(data)!=m['bytes'] or hashlib.sha256(data).hexdigest()!=m['sha256']:fail('hash/size mismatch: '+name)
for script,output in [('check_fusion.py','FUSION_CHECKS.json'),('check_obstructions.py','OBSTRUCTION_CHECKS.json')]:
    run=subprocess.run([sys.executable,'-B',str(ROOT/script)],cwd=ROOT,capture_output=True,check=False)
    if run.returncode:fail('checker failed: '+script+'\n'+run.stderr.decode())
    if run.stdout!=(ROOT/output).read_bytes():fail('checker output differs: '+script)
print(json.dumps({'status':'PASS','frozen_member_count':len(expected),'math_checks':['finite fusion morphisms','carry cocycles','wreath invariant forms','coprime cyclic modules'],'general_extension_question':'unresolved','independent_mathematical_review':'pending at author freeze'},sort_keys=True))
