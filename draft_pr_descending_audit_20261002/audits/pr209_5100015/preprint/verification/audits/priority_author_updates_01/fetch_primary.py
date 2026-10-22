"""Unauthenticated primary byte receipts; run assigned Python with -B.
All third-party bytes stay in private_reading; no downloaded code is imported.
"""
from pathlib import Path
import datetime, hashlib, json, sys, urllib.request, urllib.error
BASE = Path(__file__).resolve().parent
OUT = BASE / 'private_reading'
RECEIPT = BASE / 'SOURCE_ACCESS_RECEIPTS.json'
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(label, url):
    row = {'label':label, 'request_url':url, 'started_utc':utc(), 'authentication':'none', 'method':'GET'}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics priority audit public read-only HTTP'})
        with urllib.request.urlopen(req,timeout=40) as r:
            data=r.read()
            row.update(http_status=r.status,final_url=r.url,response_headers=dict(r.headers.items()))
        path=OUT/label
        path.write_bytes(data)
        row.update(saved_private_path=str(path),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),success=True)
    except Exception as exc:
        row.update(success=False,exception_type=type(exc).__name__,error=str(exc))
        if isinstance(exc,urllib.error.HTTPError):
            data=exc.read(); path=OUT/(label+'.http_error'); path.write_bytes(data)
            row.update(http_status=exc.code,response_headers=dict(exc.headers.items()),error_bytes=len(data),error_sha256=hashlib.sha256(data).hexdigest(),saved_private_error_path=str(path))
    row['finished_utc']=utc()
    rows=json.loads(RECEIPT.read_text()) if RECEIPT.exists() else []
    rows.append(row); RECEIPT.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in row.items() if k!='response_headers'},ensure_ascii=False))
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: fetch_primary.py private_filename URL')
    fetch(*sys.argv[1:])
