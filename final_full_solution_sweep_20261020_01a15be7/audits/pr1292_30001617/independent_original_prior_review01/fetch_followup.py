from pathlib import Path
import urllib.request,urllib.parse,json,datetime,hashlib,subprocess
p=Path(__file__).resolve().parent
urls=[('ksu_identifiers.json','https://krex.k-state.edu/server/api/core/items/fc78dcc4-94ce-4d5e-8e47-4c2ce2f235dc/identifiers'),('crossref_title_search_complete.json','https://api.crossref.org/works?query.title='+urllib.parse.quote('The law of the iterated logarithm for tail sums')+'&query.author=Ghimire&rows=30'),('upper_bounds2025.pdf','https://www.pjaa.poincarepublishers.com/pjaa/wp-content/uploads/2026/01/fp-PJAA-2025_123-9.pdf')]
rs=[]
for name,url in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior audit PR1292 (read-only source identity)'}),timeout=30) as r:
   b=r.read(1300001)
   if len(b)>1300000:raise RuntimeError('bounded source budget exceeded')
   (p/'sources'/name).write_bytes(b)
   rec.update(status=r.status,final_url=r.url,bytes=len(b),content_type=r.headers.get('Content-Type'),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:rec.update(status=getattr(e,'code',None),error=repr(e))
 rs.append(rec);(p/'FOLLOWUP_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True)
f=p/'sources/upper_bounds2025.pdf'
if f.exists() and f.read_bytes().startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
