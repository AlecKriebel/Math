from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
ROOT=Path(__file__).resolve().parent
url='https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf'
r={'actual_pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'children':[]}
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mathematical source audit'}),timeout=35) as req:
    b=req.read();r.update(final_url=req.url,content_type=req.headers.get('Content-Type'))
if not b.startswith(b'%PDF'):raise ValueError('Expected PDF')
pdf=ROOT/'private_sources/takagi2013_published.pdf';pdf.write_bytes(b)
r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for cmd,out in [(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(pdf.with_suffix('.txt'))],None),(['/opt/homebrew/bin/pdfinfo',str(pdf)],pdf.with_suffix('.pdfinfo.txt'))]:
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);a,b=p.communicate()
    r['children'].append({'actual_pid':p.pid,'argv':cmd,'exit_code':p.returncode,'stderr':b.decode()})
    if p.returncode:raise ValueError('Extraction failed')
    if out:out.write_bytes(a)
for page in [22,24,25]:
    pref=ROOT/'private_renders'/('takagi2013_published_physical_p'+str(page))
    cmd=['/opt/homebrew/bin/pdftoppm','-r','200','-f',str(page),'-l',str(page),'-singlefile','-png',str(pdf),str(pref)]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);a,b=p.communicate()
    if p.returncode:raise ValueError('Rendering failed')
    data=Path(str(pref)+'.png').read_bytes()
    r['children'].append({'actual_pid':p.pid,'argv':cmd,'exit_code':p.returncode,'stderr':b.decode(),'output':str(pref)+'.png','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'physical_page_one_based':page,'visual_read_not_yet_certified':True})
r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'TAKAGI2013_RETRIEVAL_RENDER_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'actual_pid':os.getpid(),'bytes':r['bytes'],'sha256':r['sha256'],'result':'PASS'}))
