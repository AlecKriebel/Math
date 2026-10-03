#!/usr/bin/env python3
"""Verify the full publication envelope without changing either frozen snapshot."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

base=Path(__file__).resolve().parent
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((base/'MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}|{'MANIFEST.json'}
actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
assert expected==actual,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for e in manifest['files']:
    p=base/e['path']
    assert p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],e['path']
original='93334356491d6719b98b628ebb4b011fcb6438428b46e454935d544702fd1ff7'
reviewed='23a762eb50f83e3e4cec46708b4231e7d1de23a76ef2555098ae30f376533d4f'
narrow='6cfe7b1f0c6d639b006c363cac85415a47daa96149c85eebf580f063cf9d22c6'
assert digest(base/'original/MANIFEST.json')==original
assert digest(base/'reviewed/MANIFEST.json')==reviewed
assert digest(base/'NARROW_REVIEW.md')==narrow
review=json.loads((base/'narrow_review_status.json').read_text())
assert review['verdict']=='PASS' and review['initial_hold_resolved'] is True
assert review['audited_release_manifest_sha256']==reviewed
assert review['original_author_manifest_sha256']==original
assert review['report_sha256']==narrow
status=json.loads((base/'status.json').read_text())
assert status['research_status']=='exhausted' and status['mathematical_status']=='unresolved'
assert status['substantive_attempts']==status['budget']==5
assert status['full_target_solved'] is False and status['sixth_attempt'] is False
for directory in ('original','reviewed'):
    with tempfile.TemporaryDirectory(prefix='kou-21-141-publication-') as td:
        copy=Path(td)/directory
        shutil.copytree(base/directory,copy)
        subprocess.run([sys.executable,str(copy/'verify_artifacts.py')],cwd=copy,check=True)
for e in manifest['files']:
    assert digest(base/e['path'])==e['sha256'],e['path']
print(json.dumps({'numeric_id':2650,'payload_files':len(manifest['files']),
                  'snapshot_integrity':'PASS','finite_controls':'PASS',
                  'independent_narrow_review':'PASS','full_target':'unresolved',
                  'attempts':'5/5','novelty_certified':False}))
