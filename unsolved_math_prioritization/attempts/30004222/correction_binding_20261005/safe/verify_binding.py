#!/usr/bin/env python3
"""Verify old/new hash binding and reproduce the exact unified diff."""
from pathlib import Path
import argparse,difflib,hashlib,json
ap=argparse.ArgumentParser();ap.add_argument('old');ap.add_argument('corrected');args=ap.parse_args()
here=Path(__file__).resolve().parent;old=Path(args.old);new=Path(args.corrected)
def h(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
binding=json.loads((here/'BINDING.json').read_text());inventory=json.loads((here/'CHANGE_INVENTORY.json').read_text())
assert h(old/'MANIFEST.json')==binding['original_manifest']
assert h(new/'MANIFEST.json')==binding['corrected_manifest']
for name in ['OLD_TO_NEW.diff','CHANGE_INVENTORY.json']:
 key='patch' if name.endswith('.diff') else 'change_inventory'
 assert h(here/name)=={k:binding[key][k] for k in ('bytes','sha256')}
chunks=[]
assert {p.name for p in old.iterdir()}=={x['path'] for x in inventory['changes'] if x['old'] is not None}
assert {p.name for p in new.iterdir()}=={x['path'] for x in inventory['changes'] if x['new'] is not None}
for x in inventory['changes']:
 name=x['path'];a=old/name;b=new/name
 assert (h(a) if a.exists() else None)==x['old']
 assert (h(b) if b.exists() else None)==x['new']
 if x['change']!='unchanged':
  before=a.read_text().splitlines(True) if a.exists() else []
  after=b.read_text().splitlines(True) if b.exists() else []
  chunks.extend(difflib.unified_diff(before,after,fromfile='a/'+name if a.exists() else '/dev/null',tofile='b/'+name if b.exists() else '/dev/null'))
assert ''.join(chunks).encode()==(here/'OLD_TO_NEW.diff').read_bytes()
print(json.dumps({'status':'PASS','original_binding':True,'corrected_binding':True,'exact_unified_diff':True,'inventory_entries':len(inventory['changes'])},indent=2))
