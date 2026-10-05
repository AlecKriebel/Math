#!/usr/bin/env python3
import urllib.request, json, hashlib, os
from pathlib import Path
from datetime import datetime, timezone
items=[('ht_2002_gtm','https://msp.org/gtm/2002/04/gtm-2002-04-006s.pdf','pdf'),('zhang_carey_1996','https://link.springer.com/content/pdf/10.1007/BF02506419.pdf','pdf'),('takata_1996','https://www.worldscientific.com/doi/pdf/10.1142/S0218216596000497','pdf'),('ht_final_publisher','https://www.worldscientific.com/doi/10.1142/S021821650400336X','html')]
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
Path('ADJACENT_RETRIEVAL_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
