"""Independent primary-document access; complete bodies stay in ignored private cache."""
from pathlib import Path
import datetime as dt, hashlib, json, os, urllib.request
F=Path(__file__).absolute().parent
C=F.parent/'private_primary_reading_cache/priority_audit_family'
sources=[('owr_2017.pdf','https://ems.press/doi/pdf/10.4171/OWR/2017/3'),('banakh_belegradek_v2.pdf','https://arxiv.org/pdf/1510.07269v2'),('belegradek_hu_erratum.pdf','https://link.springer.com/content/pdf/10.1007/s00208-015-1354-1.pdf')]
rows=[]
for name,url in sources:
    row=dict(url=url,started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_reader_pid=os.getpid(),private_cache_path=str(C/name),body_retained_publicly=False)
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (primary literature reading)'})
        with urllib.request.urlopen(request,timeout=45) as response:
            body=response.read();row.update(status_code=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        if not body.startswith(b'%PDF'):raise ValueError('Access response was not a PDF')
        with (C/name).open('xb') as f:f.write(body)
        row['status']='DOWNLOADED_COMPLETE_PRIMARY_PDF'
    except Exception as exc:row.update(status='ACCESS_FAILED',error=repr(exc))
    row['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat();rows.append(row)
receipt=dict(schema='pr57-priority-first-party-primary-fetch-receipts/v1',actual_reader_pid=os.getpid(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),complete_bodies_publicly_retained=False,rows=rows)
with (F/'PRIMARY_FETCH_RECEIPTS.json').open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(dict(actual_reader_pid=os.getpid(),outcomes=[{k:z[k] for k in ['url','status']} for z in rows])))
