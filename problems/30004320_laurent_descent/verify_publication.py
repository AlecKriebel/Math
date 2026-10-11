#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args();d=Path(__file__).resolve().parent
m=json.loads((d/'PUBLICATION_MANIFEST.json').read_bytes())
for row in m['files']:
 b=(d/row['path']).read_bytes();assert len(b)==row['bytes'];assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
cmd=[sys.executable,str(d/'verify_packet.py')]
if a.source_dir:cmd+=['--source-dir',str(a.source_dir.resolve())]
subprocess.run(cmd,check=True)
subprocess.run([sys.executable,str(d/'review'/'verify_review.py'),'--author-dir',str(d)],check=True)
print('PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5')
