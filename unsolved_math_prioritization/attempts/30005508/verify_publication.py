#!/usr/bin/env python3
"""Verify the exact public packet and rerun both independent finite check programs."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
count=0
def check_file(path,rec):
 global count
 b=path.read_bytes()
 assert len(b)==rec['bytes'],str(path)+' size mismatch'
 assert hashlib.sha256(b).hexdigest()==rec['sha256'],str(path)+' hash mismatch'
 count+=1
manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
expected={r['path'] for r in manifest['files']}|{'RELEASE_MANIFEST.json'}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual==expected,(sorted(actual-expected),sorted(expected-actual))
for rec in manifest['files']:check_file(ROOT/rec['path'],rec)
author=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
for rec in author['files']:check_file(ROOT/'release'/rec['path'],rec)
audit=json.loads((ROOT/'audit/AUDIT_MANIFEST.json').read_text())
for rec in audit['audit_files']:check_file(ROOT/'audit'/rec['path'],rec)
assert audit['verdict']=='PASS_SCOPED_PARTIAL'
assert audit['research_status']=='unresolved' and not audit['full_resolution_claim']
for program,record in [('release/check_exact.py','release/exact_results.json'),('audit/independent_controls.py','audit/independent_results.json')]:
 r=subprocess.run([sys.executable,str(ROOT/program)],check=True,capture_output=True)
 assert r.stdout==(ROOT/record).read_bytes(),program+' output mismatch'
 assert not r.stderr,program+' unexpected stderr'
print(json.dumps({'status':'PASS','file_hash_checks':count,'exact_full_output_replays':2,'problem_status':'unresolved','attempts_completed':5,'full_resolution_claim':False},indent=2))
