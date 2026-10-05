#!/usr/bin/env python3
import urllib.request, json, hashlib, os
from pathlib import Path
from datetime import datetime, timezone
items=[('zhang_carey_author_upload','https://www.researchgate.net/profile/Alan-Carey/publication/243194401_Quantum_groups_at_odd_roots_of_unity_and_topological_invariants_of_3-manifolds/links/0deec5298a81241fda000000/Quantum-groups-at-odd-roots-of-unity-and-topological-invariants-of-3-manifolds.pdf','pdf'),('ht_final_correct_publisher','https://www.worldscientific.com/doi/10.1142/S0218216504003342','html')]
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
Path('AUTHOR_UPLOAD_RETRIEVAL_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
