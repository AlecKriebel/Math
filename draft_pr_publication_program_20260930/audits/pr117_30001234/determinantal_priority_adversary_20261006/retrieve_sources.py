from pathlib import Path
import datetime, hashlib, json, os, subprocess, urllib.request
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'private_sources'
DEST.mkdir(exist_ok=True)
J=[]
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,url in [('docampo_1011.1930v2','https://arxiv.org/pdf/1011.1930v2'),('mustata_1107.2676v1','https://arxiv.org/pdf/1107.2676v1'),('miller_singh_varbaro_1210.6729v2','https://arxiv.org/pdf/1210.6729v2')]:
    entry={'name':name,'url':url,'started_utc':utc()}
    J.append(entry)
    req=urllib.request.Request(url,headers={'User-Agent':'Mathematical research source audit'})
    with urllib.request.urlopen(req,timeout=35) as r:
        body=r.read(); entry['final_url']=r.url;entry['content_type']=r.headers.get('Content-Type')
    if not body.startswith(b'%PDF'): raise ValueError('Expected PDF')
    pdf=DEST/(name+'.pdf')
    if pdf.exists() and pdf.read_bytes()!=body: raise ValueError('Existing source differs')
    if not pdf.exists():pdf.write_bytes(body)
    entry.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
    for cmd,out in [(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(DEST/(name+'.txt'))],None),(['/opt/homebrew/bin/pdfinfo',str(pdf)],DEST/(name+'.pdfinfo.txt'))]:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        entry.setdefault('actual_children',[]).append({'pid':p.pid,'argv':cmd})
        a,b=p.communicate();entry['actual_children'][-1].update(exit_code=p.returncode,stderr=b.decode())
        if p.returncode:raise ValueError('Extraction failed')
        if out:out.write_bytes(a)
    entry['finished_utc']=utc()
    (ROOT/'RETRIEVAL_RECEIPT.json').write_text(json.dumps({'actual_pid':os.getpid(),'sources':J},indent=2)+'\n')
print(json.dumps({'actual_pid':os.getpid(),'source_count':len(J),'result':'PASS'}))
