#!/usr/bin/env python3
"""Retrieve primary-source bodies only to ignored tmp/; record public receipt metadata."""
from pathlib import Path
import datetime, hashlib, json, urllib.request, sys
root=Path(__file__).resolve().parent
sources=json.loads((root/'FETCH_PLAN.json').read_text())
ledger_path=root/'FETCH_RECEIPTS.json'
receipts=json.loads(ledger_path.read_text()) if ledger_path.exists() else []
for s in sources:
 if s['id'] in {r['id'] for r in receipts}:continue
 r={'id':s['id'],'url':s['url'],'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0 independent primary-source scholarly review'})
  with urllib.request.urlopen(req,timeout=50) as f:b=f.read();r.update(status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'))
  suffix='.pdf' if b.startswith(b'%PDF') else '.html' if b'html' in b[:1000].lower() else '.data'
  out=root/'tmp'/(s['id']+suffix);out.write_bytes(b)
  r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),local_cache=str(out.relative_to(root)),is_pdf=b.startswith(b'%PDF'))
 except Exception as e:r['error']=repr(e)
 r['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipts.append(r)
 ledger_path.write_text(json.dumps(receipts,indent=2)+'\n');print(json.dumps(r),flush=True)
