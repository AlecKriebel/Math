#!/usr/bin/env python3
"""Readonly verifier; ROOT may copy this source outside the closed family and run it."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, sys
assert __debug__ and not sys.flags.optimize
F=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr47_2849/current_source_adversary_family')
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
mf=F/'SELF_MANIFEST.json'; b=raw(mf); m=json.loads(b)
assert m['schema']=='pr47-current-source-adversary-self-only-closure/v1' and m['self_excluded']==['SELF_MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['closed_clean'] is False and m['mandatory_corrections_count']==1 and m['current_freeze_or_merge_approved'] is False
assert stat.S_IMODE(mf.stat().st_mode)==0o444
seen=set()
for r in m['files']:
    assert type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['path']) is str and r['path'] not in seen and type(r['bytes']) is int and r['bytes']>=0 and type(r['full_mode']) is int and r['full_mode']==0o444
    n=PurePosixPath(r['path']); assert not n.is_absolute() and str(n)==r['path'] and '..' not in n.parts
    p=F/r['path']; body=raw(p); assert len(body)==r['bytes'] and sha(body)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444; seen.add(r['path'])
fs=set(); ds=set()
for p in F.rglob('*'):
    assert not p.is_symlink(); n=p.relative_to(F).as_posix()
    if stat.S_ISDIR(p.stat().st_mode): ds.add(n)
    else: assert stat.S_ISREG(p.stat().st_mode); fs.add(n)
assert fs==seen|{'SELF_MANIFEST.json'} and ds==set(m['directories']) and ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'}
v=json.loads(raw(F/'VERDICT.json')); report=raw(F/'REPORT.md')
assert v['closed_clean'] is False and v['mandatory_corrections'][0]['line']==150 and v['positive_assertions']==31826 and sha(report)==v['report']['sha256'] and len(report)==v['report']['bytes']
print(json.dumps({'status':'PASS_READONLY_CLOSED_ADVERSE_SOURCE_FAMILY','manifest_sha256':sha(b),'payload_files':len(seen),'directories':len(ds),'report_sha256':sha(report),'mandatory_corrections_count':1,'production_or_current_merge_approved':False},indent=2))
