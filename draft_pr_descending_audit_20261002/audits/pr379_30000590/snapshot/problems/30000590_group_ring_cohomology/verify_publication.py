#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args();d=Path(__file__).resolve().parent
for mn,base in [('PUBLICATION_MANIFEST.json',d),('review/REVIEW_MANIFEST.json',d/'review')]:
 for f in json.loads((d/mn).read_bytes())['files']:
  b=(base/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
for n,h in {'FINAL_AUTHOR_MANIFEST.json':'a8881d305f9fa739590bfe47b8bd8ef6b28027e9523102498621e94c9085e255','REVIEW_CORRECTION_MANIFEST.json':'76d2ab2d1dcbb83b71ed87d8e60b75ad198e0c54554fa583a1803550a5cf3fa7','review/REVIEW_MANIFEST.json':'e37355d91be863eb160f8d16cfe4473455b9943268699f65c79b37a389a0b1d3'}.items():
 assert hashlib.sha256((d/n).read_bytes()).hexdigest()==h
cmd=[sys.executable,str(d/'verify_packet.py')]
if a.source_dir:cmd+=['--source-dir',str(a.source_dir.resolve())]
subprocess.run(cmd,check=True)
subprocess.run([sys.executable,str(d/'review/verify_review.py'),'--author',str(d)],check=True)
print('PASS: preserved author/correction/review bytes, 747103 author and 23463 independent controls; original unsolved 5/5')
