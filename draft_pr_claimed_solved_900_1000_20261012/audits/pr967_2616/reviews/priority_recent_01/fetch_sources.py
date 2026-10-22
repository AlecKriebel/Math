#!/usr/bin/env python3
"""Read-only HTTP source capture into this audit's private_primary directory.
Usage: python3 fetch_sources.py SOURCE_ID URL [FILENAME]
Public receipts contain only URL/date/status/bytes/hash, never source bodies.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys, urllib.request
root=Path(__file__).resolve().parent
ident,url=sys.argv[1:3]
filename=sys.argv[3] if len(sys.argv)>3 else ident+'.html'
dest=root/'private_primary'/filename
dest.parent.mkdir(mode=0o700,exist_ok=True)
r={'id':ident,'requested_url':url,'started_utc':datetime.now(timezone.utc).isoformat()}
try:
 request=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical literature audit (read-only)'})
 with urllib.request.urlopen(request,timeout=50) as response:
  body=response.read()
  r.update(final_url=response.url,status=response.status,content_type=response.headers.get('Content-Type'),last_modified=response.headers.get('Last-Modified'))
 dest.write_bytes(body); dest.chmod(0o600)
 r.update(filename='private_primary/'+filename,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),success=True)
except Exception as e:r.update(success=False,error=str(e))
r['completed_utc']=datetime.now(timezone.utc).isoformat()
with (root/'SOURCE_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps(r,sort_keys=True)+'\n')
print(json.dumps(r,sort_keys=True))
