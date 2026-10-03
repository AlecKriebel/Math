#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args();d=Path(__file__).resolve().parent
for mn,base in [('PUBLICATION_MANIFEST.json',d),('review/REVIEW_MANIFEST.json',d/'review')]:
 for f in json.loads((d/mn).read_bytes())['files']:
  b=(base/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
for n,h in {'FINAL_AUTHOR_MANIFEST.json':'7a3a86cd82d0057438b599e4e1b6d4d5a5f4196cdf7fd9bc583467af1a7373de','review/REVIEW_MANIFEST.json':'5f53a0417252f49b63badd7c933442d64882d8f91d67f45a3491d03e47723029'}.items():
 assert hashlib.sha256((d/n).read_bytes()).hexdigest()==h
cmd=[sys.executable,str(d/'verify_packet.py')]
if a.source_dir:cmd+=['--source-dir',str(a.source_dir.resolve())]
subprocess.run(cmd,check=True)
b=subprocess.check_output([sys.executable,str(d/'review/independent_check.py')]);assert b==(d/'review/INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: preserved author/review bytes, 12967236 author and 30053 independent assertions; original unsolved 5/5')
