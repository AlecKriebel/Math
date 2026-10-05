#!/usr/bin/env python3
import urllib.request, json, hashlib, os
from pathlib import Path
from datetime import datetime, timezone
items=[('gang_abs','https://arxiv.org/abs/0912.4664','html'),('gang_v1','https://arxiv.org/pdf/0912.4664v1','pdf'),('kubo_yokoyama_abs','https://arxiv.org/abs/2108.09300','html'),('kubo_yokoyama_v1','https://arxiv.org/pdf/2108.09300v1','pdf')]
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
Path('LATER_RETRIEVAL_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
