#!/usr/bin/env python3
"""Fresh full original remote file bodies; reads only, raw API kept private."""
import base64, hashlib, json
from capture import ROOT,run,now
receipt=json.loads((ROOT/'03_reproduction_bindings.json').read_text())
for i,entry in enumerate(receipt['original_bindings']):
    p=run('api_content_'+str(i).zfill(2),['gh','api','repos/AlecKriebel/Math/contents/'+entry['path']+'?ref='+receipt['frozen_head']],'/Users/alec/Documents/Math')
    assert p.returncode==0 and p.stderr==b''
    obj=json.loads(p.stdout);b=base64.b64decode(obj['content'])
    assert obj['path']==entry['path'] and obj['sha']==entry['git_blob'] and obj['size']==entry['bytes']
    assert b==(ROOT.parent/'snapshot'/entry['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==entry['sha256']
print(json.dumps(dict(completed_utc=now(),full_api_file_bodies=19,all_original_Git_API_snapshot_equal=True),indent=2))
