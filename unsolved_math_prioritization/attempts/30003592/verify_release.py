#!/usr/bin/env python3
"""Read-only final-layout integrity and replay wrapper. No network actions."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--integrity-only',action='store_true')
parser.add_argument('--archive',type=Path)
args=parser.parse_args()
manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
expected=manifest['files']
entries=list(ROOT.rglob('*'))
assert all(not p.is_symlink() for p in entries),'symlink rejected'
assert {p.relative_to(ROOT).as_posix() for p in entries if p.is_dir()}=={'submission','independent-audit'},'directory allowlist'
files={p.relative_to(ROOT).as_posix():p for p in entries if p.is_file() and p!=ROOT/'RELEASE_MANIFEST.json'}
assert set(files)==set(expected),'exact file allowlist'
for name,p in files.items():
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected[name]['sha256'],name
 assert p.stat().st_size==expected[name]['bytes'],name
if args.integrity_only:
 print(json.dumps({'integrity_passed':True,'files_checked':len(files),'self_excluded':'RELEASE_MANIFEST.json'}))
 sys.exit(0)

def run(path,*extra):
 p=subprocess.run([sys.executable,str(path),*map(str,extra)],cwd=path.parent,capture_output=True,text=True)
 if p.returncode:raise AssertionError((path.name,p.stdout,p.stderr))
 return json.loads(p.stdout)

author=run(ROOT/'submission/verify.py')
assert author['all_passed'] and author['exact_checks']==1877
author_manifest=run(ROOT/'submission/verify_manifest.py')
assert author_manifest['manifest_passed'] and author_manifest['files_checked']==11
binding=json.loads((ROOT/'independent-audit/AUDITED_INPUT_MANIFEST.json').read_text())
with tempfile.TemporaryDirectory() as td:
 archive=args.archive
 if archive is None:
  archive=Path(td)/'rank631-30003592-authored-packet.zip'
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for name in sorted(binding['submission_file_sha256']):
    info=zipfile.ZipInfo('submission/'+name,date_time=(2026,10,4,14,28,44))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=(0o644<<16)
    z.writestr(info,(ROOT/'submission'/name).read_bytes())
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==binding['archive_sha256'],'original ZIP digest differs; provide --archive with the exact original ZIP'
 audit=run(ROOT/'independent-audit/independent_checks.py','--submission',ROOT/'submission','--archive',archive,'--replay')
assert audit['all_passed'] and audit['checks']==2003
nonmath={'archive_integrity','audit_integrity','frozen_integrity','supplied_replay'}
math_checks=sum(v for k,v in audit['groups'].items() if k not in nonmath)
assert math_checks==1961
print(json.dumps({'all_passed':True,'status':'unsolved','publication_files':len(files)+1,'original_checks':1877,'audit_checks':2003,'audit_math_checks':1961,'audit_integrity_and_replay_checks':42,'formal_geometric_proof':False},indent=2))
