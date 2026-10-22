#!/usr/bin/env python3
"""Read-only receipt authentication. --public-only explicitly skips private bodies."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--public-only',action='store_true');a=p.parse_args()
base=Path(__file__).resolve().parent
r=json.loads((base/'RECEIPT.json').read_text());verified=0;skipped=0
for group in ('inputs','authored_artifacts','private_source_material'):
 for pin in r[group]:
  if a.public_only and group=='private_source_material':skipped+=1;continue
  b=(base/pin['path']).read_bytes()
  if len(b)!=pin['bytes'] or hashlib.sha256(b).hexdigest()!=pin['sha256']:raise ValueError('integrity failure: '+pin['path'])
  verified+=1
print(json.dumps({'status':'PASS','verified_files':verified,'explicitly_skipped_private_source_files':skipped},sort_keys=True))
