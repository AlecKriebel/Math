"""Ordinary public read-only GETs for exact pinned primary proof bytes."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import urllib.request

LANE=Path(__file__).resolve().parent
SOURCE=LANE.parents[1]/'sources/archives/01-source-and-verification.zip.extracted'
manifest=json.loads((SOURCE/'provenance/manuscript_source_hashes.json').read_text())
COMMIT=manifest['pinned_commit']
DEST=LANE/'primary-pinned'
DEST.mkdir(exist_ok=False)

def get(item):
    relative=item['path']
    url=f'https://raw.githubusercontent.com/openai/math/{COMMIT}/{relative}'
    started=datetime.now(timezone.utc).isoformat()
    request=urllib.request.Request(url,headers={'User-Agent':'Independent-source-review/1.0'})
    with urllib.request.urlopen(request,timeout=60) as response:
        data=response.read(); status=response.status; headers=dict(response.headers.items())
    actual=hashlib.sha256(data).hexdigest()
    assert len(data)==item['bytes'] and actual==item['sha256'],(relative,len(data),actual)
    target=DEST/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    return {'path':relative,'url':url,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'status':status,'headers':headers,'bytes':len(data),'sha256':actual,'matches_published_provenance':True}

with ThreadPoolExecutor(max_workers=4) as executor:
    results=list(executor.map(get,manifest['files']))
(LANE/'PRIMARY_ACQUISITION.json').write_text(json.dumps({'commit':COMMIT,'ordinary_public_GET_only':True,'files':results},indent=2)+'\n')
print(json.dumps({'files':len(results),'all_exact':True,'commit':COMMIT}))
