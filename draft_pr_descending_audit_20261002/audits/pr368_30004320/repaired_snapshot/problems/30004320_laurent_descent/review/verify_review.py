#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,required=True);a=p.parse_args();d=Path(__file__).resolve().parent
for r in json.loads((d/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(d/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']
assert hashlib.sha256((a.author_dir/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='aa4ebd52776b5f6dbd8dbf95853f3af85851d6b194402e44797ddbbf31f2a1ee'
for r in json.loads((d/'REMOTE_BINDING.json').read_text())['files']:
 b=(a.author_dir/r['path']).read_bytes();assert len(b)==r['size'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha']
assert subprocess.check_output([sys.executable,str(d/'independent_checks.py')])==(d/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: review hashes, frozen author/remote binding, and independent replay')
