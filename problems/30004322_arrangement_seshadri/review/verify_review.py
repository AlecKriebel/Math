#!/usr/bin/env python3
"""Portable review verification. Python3 plus SymPy; sources optional and reported."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,required=True);a=p.parse_args();D=Path(__file__).resolve().parent
for r in json.loads((D/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(D/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']
assert hashlib.sha256((a.author_dir/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='7df340e34bab39476fcafb29c1f980617c477f698d06ed9fb18f931367ccb101'
for r in json.loads((D/'REMOTE_BINDING.json').read_text())['files']:
 b=(a.author_dir/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['expected_git_blob']==r['remote_git_blob']
r=json.loads(subprocess.check_output([sys.executable,str(a.author_dir/'REPLAY_ALL.py')],cwd=a.author_dir))
assert r['assertions']==214070 and r['manifest_entries']==62 and r['all_receipts_byte_exact']
assert r['source_files_checked']==(6 if (a.author_dir/'sources').is_dir() else 0)
assert subprocess.check_output([sys.executable,str(D/'independent_checks.py')])==(D/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps({'review':'PASS','author_assertions':214070,'independent_assertions':93918,'source_files_checked':r['source_files_checked'],'source_note':'Source bindings verified' if r['source_files_checked'] else 'Raw source files absent; source verification explicitly omitted'},sort_keys=True))
