"""Two exact primary-document GETs after preserving the archive's non-PDF response."""
import datetime, hashlib, json, subprocess, urllib.request
from pathlib import Path
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204212/reviews/scope-continuation-20261117')
items=[('CFP-author-archived-1996.pdf','https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf'),('Moore-published-2013.pdf','https://www.impan.pl/shop/en/publication/transaction/download/product/88935')]
records=[]
for name,url in items:
    row=dict(name=name,URL=url,started_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(url,timeout=60) as r:body=r.read();row.update(status_code=r.status,effective_URL=r.url,headers=list(r.headers.items()))
        p=OWN/'primary/classical'/name
        with p.open('xb') as f:f.write(body)
        row.update(bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),PDF_signature=body.startswith(b'%PDF-'))
        assert row['PDF_signature']
        argv=['/opt/homebrew/bin/pdftotext','-layout',str(p),str(p.with_suffix('.txt'))]
        with p.with_suffix('.pdftotext.stdout').open('xb') as out,p.with_suffix('.pdftotext.stderr').open('xb') as err:r=subprocess.run(argv,stdout=out,stderr=err,check=False)
        row.update(pdftotext_argv=argv,pdftotext_exit=r.returncode,status='RETRIEVED')
    except Exception as e:row.update(status='FAILED_LITERAL_NO_RETRY',error_type=type(e).__name__,error=str(e))
    row['finished_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();records.append(row)
with (OWN/'CLASSICAL_SUPPLEMENT_RETRIEVAL.json').open('x') as f:json.dump(dict(records=records,prior_nonPDF_response_and_old_retriever_preserved=True,each_URL_attempts=1),f,indent=2);f.write('\n')
print(json.dumps(records))
