"""Additive primary access attempts; earlier receipts/source remain unchanged."""
from pathlib import Path
import datetime as dt,hashlib,json,os,urllib.request
F=Path(__file__).absolute().parent;C=F.parent/'private_primary_reading_cache/priority_audit_family'
sources=[('banakh_belegradek_jstage.pdf','https://www.jstage.jst.go.jp/article/jmath/70/2/70_733/_pdf/-char/en'),('mateljevic_endpoint_arxiv.pdf','https://arxiv.org/pdf/2208.02551'),('plotnikov_russian.pdf','https://www.mathnet.ru/php/getFT.phtml?jrnid=tm&option_lang=eng&paperid=4443&what=fullt'),('peters_1987.pdf','https://www.numdam.org/article/CM_1987__62_1_3_0.pdf')]
rows=[]
for name,url in sources:
    z=dict(url=url,started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_reader_pid=os.getpid(),private_cache_path=str(C/name),body_retained_publicly=False)
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=30) as r:b=r.read();z.update(status_code=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
        if not b.startswith(b'%PDF'):raise ValueError('Response is not PDF')
        with (C/name).open('xb') as f:f.write(b)
        z['status']='DOWNLOADED_COMPLETE_PRIMARY_PDF'
    except Exception as e:z.update(status='ACCESS_FAILED',error=repr(e))
    z['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat();rows.append(z)
with (F/'LATEST_PRIMARY_FETCH_RECEIPTS.json').open('x') as f:json.dump(dict(schema='pr57-priority-latest-primary-access/v1',actual_reader_pid=os.getpid(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows),f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(dict(actual_reader_pid=os.getpid(),outcomes=[dict(url=z['url'],status=z['status']) for z in rows])))
