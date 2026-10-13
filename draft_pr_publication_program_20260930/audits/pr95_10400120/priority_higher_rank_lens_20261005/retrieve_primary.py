#!/usr/bin/env python3
import urllib.request, json, hashlib, os
from pathlib import Path
from datetime import datetime, timezone
items=[('ht_abs_v1','https://arxiv.org/abs/math/0209403v1','html'),('ht_abs_v2','https://arxiv.org/abs/math/0209403v2','html'),('ht_v1','https://arxiv.org/pdf/math/0209403v1','pdf'),('zhang_abs','https://arxiv.org/abs/q-alg/9612034','html'),('zhang_v1','https://arxiv.org/pdf/q-alg/9612034v1','pdf')]
ledger=[]
for name,url,extension in items:
 t=datetime.now(timezone.utc).isoformat(); entry={'name':name,'url':url,'UTC':t,'PID':os.getpid()}
 try:
  with urllib.request.urlopen(url,timeout=45) as response:
   b=response.read();entry.update({'final_url':response.url,'status':response.status,'headers':dict(response.headers)})
  path=Path('private_sources')/(name+'.'+extension);path.write_bytes(b)
  entry.update({'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 except Exception as e:entry['error']=str(e)
 ledger.append(entry); print(json.dumps(entry),flush=True)
Path('RETRIEVAL_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
