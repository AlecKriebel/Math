#!/usr/bin/env python3
"""Portable verification of the reviewed, corrected partial-result release."""
import hashlib,json,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
manifest=json.loads((p/'MANIFEST.json').read_text())
for rec in manifest['files']:
 f=p/rec['path'];assert f.stat().st_size==rec['bytes'] and h(f)==rec['sha256'],rec['path']
frozen=p/'frozen_original';assert h(frozen/'AUTHOR_MANIFEST.json')=='9e0722156cc50db5ed6e178b424c270c644ad3d898e182da7c548ee478054529'
original=json.loads((frozen/'AUTHOR_MANIFEST.json').read_text())
for rec in original['files']:
 f=frozen/rec['path'];assert f.stat().st_size==rec['bytes'] and h(f)==rec['sha256'],rec['path']
assert h(p/'audit/AUDIT_REPORT.md')=='df0db89b77353ac68fa5cbaa7bdfe1597d934cff3037cd6a8de6aa3b5f25a9f7'
old='More generally, if a finite abelian H acts semisimply on M, then H has limit 1 and G has limit max_i |H/K_i|, an integer.'
new='More generally, if a finite abelian H acts semisimply on nonzero M, then a nontrivial H has limit 1, while H=1 has limit 0. In either case G has limit max_i |H/K_i|, an integer (equal to 1 when H=1).'
s=(frozen/'turn_03.md').read_text();assert s.count(old)==1
assert (p/'turn_03.md').read_text()==s.replace(old,new)
for i in [1,2,4,5]:assert (p/f'turn_{i:02}.md').read_bytes()==(frozen/f'turn_{i:02}.md').read_bytes()
for f in (frozen/'checks').iterdir():
 if f.is_file():assert f.read_bytes()==(p/'checks'/f.name).read_bytes()
status=json.loads((p/'status.json').read_text());assert status['author_status']=='unsolved' and status['substantive_turns']==5 and not status['complete_resolution']
subprocess.run([sys.executable,str(p/'checks/run_all.py')],check=True)
for rec in manifest['files']:assert h(p/rec['path'])==rec['sha256'],rec['path']
print(json.dumps({'release_hashes':'PASS','original_freeze':'PASS','minor_correction_only':'PASS','exact_replay':'PASS','original_problem':'UNSOLVED_5_OF_5'},indent=2))
