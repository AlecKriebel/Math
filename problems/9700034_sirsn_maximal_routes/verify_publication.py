#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args();d=Path(__file__).resolve().parent
for mn,base in [('PUBLICATION_MANIFEST.json',d),('review/REVIEW_MANIFEST.json',d/'review')]:
 for f in json.loads((d/mn).read_bytes())['files']:
  b=(base/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
assert hashlib.sha256((d/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='e2cc5d80eb13cd4765389af0b7d9838c89752ca16758d240801880e4feefce1f'
assert hashlib.sha256((d/'review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='6392dc91cc9111c02618a412fd83e7f29002be9301387076a55e0201f8343c7a'
cmd=[sys.executable,str(d/'verify_packet.py')]
if a.source_dir:cmd+=['--source-dir',str(a.source_dir.resolve())]
subprocess.run(cmd,check=True)
b=subprocess.check_output([sys.executable,str(d/'review/independent_check.py')])
assert b==(d/'review/INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: all publication bytes, frozen author replays and 2507 independent controls; original unsolved 5/5')
