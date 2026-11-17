"""One bounded read-only primary retrieval, immutable source pins, and passive PDF text extraction."""
import concurrent.futures, datetime, hashlib, json, subprocess, time, urllib.request
from pathlib import Path, PurePosixPath

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'papers/23204212/reviews/scope-continuation-20261117'
NATIVE=P/'papers/23204212/sources/archives/01-thompson-cstar-verification.zip.extracted/sources/SOURCE_MANIFEST.json'
PIN='adc7f1241b42e322a6451854ab7e4b4c146bf78a'
PRIMARY=OWN/'primary'
PRIMARY.mkdir()
requests=[
 dict(path='classical/LMB-published-2018.pdf',URL='https://www.numdam.org/item/10.24033/asens.2361.pdf',edition='Published Annales ENS51(2018),557–602'),
 dict(path='classical/BKKO-published-2017.pdf',URL='https://www.numdam.org/item/10.1007/s10240-017-0091-2.pdf',edition='Published IHES126(2017),35–71'),
 dict(path='classical/HO-arxiv-1609.05086v1.pdf',URL='https://arxiv.org/pdf/1609.05086v1',edition='arXiv1609.05086v1,16September2016'),
 dict(path='classical/HO-published-2017.pdf',URL='https://www.isibang.ac.in/~soumyashant/misc/collected-works-of-haagerup/2010s/2017_Non-inner_amenability_of_the_Thompson_groups_T_and_V.pdf',edition='Published JFA272(2017),4838–4852; archived primary paper'),
 dict(path='classical/Brin-published-1996.pdf',URL='https://www.numdam.org/item/PMIHES_1996__84__5_0.pdf',edition='Published IHES84(1996),5–33'),
 dict(path='classical/BCR-arxiv-0711.0919v3.pdf',URL='https://arxiv.org/pdf/0711.0919v3',edition='arXiv0711.0919v3,9May2008'),
 dict(path='classical/BCR-arxiv-0711.0919v4.pdf',URL='https://arxiv.org/pdf/0711.0919v4',edition='arXiv0711.0919v4,20March2010'),
 dict(path='classical/CFP-published-1996.pdf',URL='https://www.e-periodica.ch/cntmng?pid=ens-001%3A1996%3A42%3A%3A88',edition='Published EnseignementMath42(1996),215–256; official archival PDF'),
]
native=json.loads(NATIVE.read_bytes());assert native['upstream_commit']==PIN
for row in native['files']:
    path=row['path'];parts=PurePosixPath(path).parts
    assert parts and not path.startswith('/') and all(x not in ('','.','..') for x in path.split('/'))
    requests.append(dict(path='upstream/'+path,URL='https://raw.githubusercontent.com/openai/math/'+PIN+'/'+path,edition='Exact immutable OpenAI snapshot '+PIN,expected_bytes=row['bytes'],expected_SHA256=row['sha256']))
assert len({r['path'] for r in requests})==len(requests)
with (OWN/'RETRIEVAL_PLAN.json').open('x') as f:json.dump(dict(upstream_pin=PIN,native_manifest_pin=dict(bytes=NATIVE.stat().st_size,SHA256=hashlib.sha256(NATIVE.read_bytes()).hexdigest()),requests=requests),f,indent=2);f.write('\n')
def fetch(row):
    item=dict(row,started_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat());t=time.monotonic()
    try:
        req=urllib.request.Request(row['URL'],headers={'User-Agent':'Independent mathematical source review; read-only retrieval'})
        with urllib.request.urlopen(req,timeout=60) as response:
            body=response.read();item.update(status_code=response.status,effective_URL=response.url,headers=list(response.headers.items()))
        path=PRIMARY/row['path'];path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f:f.write(body)
        item.update(bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),PDF_signature=body.startswith(b'%PDF-'))
        if 'expected_SHA256' in row:assert len(body)==row['expected_bytes'] and item['SHA256']==row['expected_SHA256']
        if row['path'].endswith('.pdf'):assert item['PDF_signature']
        item['status']='RETRIEVED_AND_IDENTITY_VALIDATED'
    except Exception as e:
        item.update(status='FAILED_LITERAL_NO_RETRY',error_type=type(e).__name__,error=str(e))
    item.update(finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t)
    return item
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,requests))
with (OWN/'PRIMARY_RETRIEVAL.json').open('x') as f:json.dump(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),upstream_pin=PIN,results=results,retrieval_attempts_per_URL=1,network_read_only=True),f,ensure_ascii=False,indent=2);f.write('\n')
calls=[]
for row in results:
    if row['status']!='RETRIEVED_AND_IDENTITY_VALIDATED' or not row['path'].endswith('.pdf'):continue
    pdf=PRIMARY/row['path'];outpath=pdf.with_suffix('.txt')
    argv=['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(outpath)]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    with pdf.with_suffix('.pdftotext.stdout').open('xb') as out,pdf.with_suffix('.pdftotext.stderr').open('xb') as err:r=subprocess.run(argv,cwd=OWN,stdout=out,stderr=err,check=False)
    calls.append(dict(argv=argv,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=r.returncode,stdout_bytes=pdf.with_suffix('.pdftotext.stdout').stat().st_size,stderr_bytes=pdf.with_suffix('.pdftotext.stderr').stat().st_size,text_bytes=outpath.stat().st_size if outpath.exists() else None))
with (OWN/'PRIMARY_PDF_TEXT_RECEIPT.json').open('x') as f:json.dump(dict(calls=calls,scientific_execution=False),f,indent=2);f.write('\n')
print(json.dumps(dict(requests=len(results),retrieved=sum(r['status']=='RETRIEVED_AND_IDENTITY_VALIDATED' for r in results),failures=[dict(path=r['path'],error=r.get('error')) for r in results if r['status']!='RETRIEVED_AND_IDENTITY_VALIDATED'],PDF_text_calls=len(calls),PDF_text_failures=[r for r in calls if r['exit_code']!=0],upstream_pin=PIN)))
