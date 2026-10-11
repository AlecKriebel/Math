#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,required=True);a=p.parse_args();D=Path(__file__).resolve().parent
for r in json.loads((D/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(D/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']
assert hashlib.sha256((a.author_dir/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='48fce3e6630fd1bfd81c49054ab4c5640eeb7079f2bd6cc62b65ea479750d78c'
for r in json.loads((D/'REMOTE_BINDING.json').read_text())['files']:
 b=(a.author_dir/r['path']).read_bytes();assert len(b)==r['size'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha']
assert subprocess.check_output([sys.executable,str(D/'independent_checks.py')])==(D/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: review, frozen author/remote bindings and independent exact replay')
