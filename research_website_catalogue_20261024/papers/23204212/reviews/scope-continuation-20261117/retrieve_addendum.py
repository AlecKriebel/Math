"""Read-only primary GET for the addendum actually used by LMB Corollary4.4."""
import datetime, hashlib, json, subprocess, urllib.request
from pathlib import Path
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204212/reviews/scope-continuation-20261117')
url='https://arxiv.org/pdf/1301.0616v1'
p=OWN/'primary/classical/BCR-addendum-1301.0616v1.pdf'
row=dict(URL=url,started_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
try:
    with urllib.request.urlopen(url,timeout=60) as r:body=r.read();row.update(status_code=r.status,effective_URL=r.url,headers=list(r.headers.items()))
    with p.open('xb') as f:f.write(body)
    row.update(bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),PDF_signature=body.startswith(b'%PDF-'));assert row['PDF_signature']
    argv=['/opt/homebrew/bin/pdftotext','-layout',str(p),str(p.with_suffix('.txt'))]
    with p.with_suffix('.pdftotext.stdout').open('xb') as out,p.with_suffix('.pdftotext.stderr').open('xb') as err:r=subprocess.run(argv,stdout=out,stderr=err,check=False)
    row.update(pdftotext_argv=argv,pdftotext_exit=r.returncode,status='RETRIEVED')
except Exception as e:row.update(status='FAILED_LITERAL_NO_RETRY',error_type=type(e).__name__,error=str(e))
row['finished_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OWN/'BCR_ADDENDUM_RETRIEVAL.json').open('x') as f:json.dump(row,f,indent=2);f.write('\n')
print(json.dumps(row))
