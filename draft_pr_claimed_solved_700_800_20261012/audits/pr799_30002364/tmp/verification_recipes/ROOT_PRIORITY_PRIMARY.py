from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, urllib.request
T=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364/tmp')
B=T/'primary-root'
specs=[('Ribet_1980','https://www.numdam.org/article/MSMF_1980_2_2__75_0.pdf'),
       ('AFV_2024_v1','https://arxiv.org/pdf/2412.03358v1'),
       ('Agugliaro_final','https://ems.press/content/serial-article-files/53071?nt=1'),
       ('Tate_352','https://www.numdam.org/article/SB_1968-1969__11__95_0.pdf')]
def fetch(spec):
    name,url=spec
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/pdf'})
    with urllib.request.urlopen(request,timeout=90) as response:
        raw=response.read(); final=response.url
    if not raw.startswith(b'%PDF'): raise ValueError('Expected primary PDF: '+name)
    pdf=B/(name+'.pdf'); txt=B/(name+'.txt')
    if pdf.exists() and pdf.read_bytes()!=raw: raise ValueError('Never replace different source bytes')
    pdf.write_bytes(raw)
    subprocess.run(['pdftotext','-layout',str(pdf),str(txt)],check=True,capture_output=True)
    return {'file':pdf.name,'url':url,'final_url':final,'bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),
            'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'reading_scope':'retrieval only; separate subsequent reading receipt'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(fetch,specs))
receipt={'result':'PASS','records':rows,'redistribute_primary_PDFs':False}
(T/'root-receipts/ROOT_PRIORITY_PRIMARY_RETRIEVAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
