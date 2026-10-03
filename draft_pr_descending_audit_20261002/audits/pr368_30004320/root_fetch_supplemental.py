"""Fresh primary acquisition from original source routing only, after source baseline and candidate mathematical prose, before verdict seal."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'snapshot/problems/30004320_laurent_descent';S=A/'raw_sources';S.mkdir(exist_ok=True)
rows=[]
for name in ['SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
    rows += json.loads((D/name).read_bytes())['files']
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(e):
    name=e['name'];assert Path(name).name==name and name.endswith('.pdf')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(urllib.request.Request(e['url'],headers={'User-Agent':'Independent mathematical source audit'}),timeout=60) as r:
        raw=r.read();url=r.geturl()
    f=S/name;f.write_bytes(raw);t=f.with_suffix('.txt')
    p=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(f),str(t)],capture_output=True)
    assert p.returncode==0,(name,p.stderr);text=t.read_bytes()
    return {'name':name,'url':e['url'],'final_url':url,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(raw),'sha256':sha(raw),'historical_pdf_bytes_equal':len(raw)==e['bytes'],'historical_pdf_sha256_equal':sha(raw)==e['sha256'],'text_bytes':len(text),'text_sha256':sha(text),'pdftotext_exit':p.returncode,'stderr':p.stderr.decode()}
results=list(concurrent.futures.ThreadPoolExecutor(5).map(fetch,rows))
(A/'root_supplemental_fetch_receipt.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
