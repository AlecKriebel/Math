"""Read-only primary acquisition; published metadata only, private raw assets."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent;S=A/'raw_sources';S.mkdir(exist_ok=True)
(A/'.gitignore').write_text('raw_sources/\ntmp/\n__pycache__/\n')
routing=json.loads((A/'snapshot/problems/30004811_capacity_volume_mass/SOURCE_MANIFEST.json').read_bytes())
def collect(v):
    out=[]
    if isinstance(v,dict):
        if 'name' in v and 'url' in v and v['name'].endswith('.pdf'):out.append(v)
        for x in v.values():out.extend(collect(x))
    elif isinstance(v,list):
        for x in v:out.extend(collect(x))
    return out
sources=collect(routing);assert len(sources)==7
def fetch(row):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(row['url'],timeout=45) as response:
        b=response.read();final=response.url
    assert b.startswith(b'%PDF-'),row['name'];(S/row['name']).write_bytes(b)
    text=(S/row['name']).with_suffix('.txt')
    r=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(S/row['name']),str(text)],capture_output=True)
    assert r.returncode==0,(row['name'],r.stderr);tb=text.read_bytes()
    digest=hashlib.sha256(b).hexdigest()
    return {'name':row['name'],'url':row['url'],'final_url':final,'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(b),'sha256':digest,'text_bytes':len(tb),'text_sha256':hashlib.sha256(tb).hexdigest(),'historical_pdf_sha_equal':digest==row['sha256'],'historical_pdf_size_equal':len(b)==row['bytes'],'pdftotext_exit':r.returncode,'stderr':r.stderr.decode()}
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(fetch,sources))
(A/'root_primary_fetch_receipt.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'primary_pdfs':len(rows),'historical_exact_matches':sum(r['historical_pdf_sha_equal'] and r['historical_pdf_size_equal'] for r in rows),'source_only_no_candidate_math_read':True},indent=2))
