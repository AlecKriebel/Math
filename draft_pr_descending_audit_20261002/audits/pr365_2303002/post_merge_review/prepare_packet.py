#!/usr/bin/env python3
"""Writing acquisition driver, never replayed as a read-only check."""
import gzip,json,pathlib
from capture import ROOT,sha
A=ROOT.parent
review=ROOT/'root_review';review.mkdir(exist_ok=True)
names=['root_verify_closed_whole.py','root_verify_closed_whole.failed01.py','ROOT_TRUNCATED_API_REPLAY_FAILURE.json','root_whole_verification_receipt.json']
pins={}
for name in names:
    b=(A/name).read_bytes();dest=review/(name+'.gz' if name.endswith('.json') else name)
    dest.write_bytes(gzip.compress(b,mtime=0) if name.endswith('.json') else b)
    pins[name]=dict(path=dest.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
# Lossless compression and relocation of this review's complete check list.
p=ROOT/'REPAIR_AND_CLOSURES.json';b=p.read_bytes();q=p.with_suffix('.json.gz');q.write_bytes(gzip.compress(b,mtime=0))
pins[p.name]=dict(path=q.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
p.unlink()
(review/'ACQUISITION_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
# ROOT evidence is optional as one complete external group, never partly accepted.
r=json.loads((A/'root_whole_verification_receipt.json').read_bytes());paths=set()
for c in r['captures']:
    paths.update(s['path'] for s in c['streams'].values())
    if 'complete_fixed_local_tree_capture' in c:paths.add(c['complete_fixed_local_tree_capture']['path'])
f=json.loads((A/'ROOT_TRUNCATED_API_REPLAY_FAILURE.json').read_bytes())
paths.update(s['new_path'] for s in f['lossless_relocation_map'].values())
inventory={}
for path in sorted(paths):
    b=(A/path).read_bytes();row=dict(bytes=len(b),sha256=sha(b))
    if path.endswith('.gz'):
        d=gzip.decompress(b);row.update(logical_bytes=len(d),logical_sha256=sha(d))
    inventory[path]=row
(ROOT/'EXTERNAL_PRIVATE.json').write_text(json.dumps(dict(files=inventory),indent=2)+'\n')
print(json.dumps(dict(acquired=pins,external_files=len(inventory)),indent=2))
