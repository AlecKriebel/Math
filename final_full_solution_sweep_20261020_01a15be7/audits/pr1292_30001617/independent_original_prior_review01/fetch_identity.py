from pathlib import Path
import urllib.request,urllib.parse,json,datetime,hashlib,subprocess,time
P=Path(__file__).resolve().parent
sources=[
('thesis_ksu_item.json','https://krex.k-state.edu/server/api/core/items/fc78dcc4-94ce-4d5e-8e47-4c2ce2f235dc'),
('crossref_title_search.json','https://api.crossref.org/works?query.title='+urllib.parse.quote('The law of the iterated logarithm for tail sums')+'&query.author=Ghimire&rows=8'),
('datacite_title_search.json','https://api.datacite.org/dois?query='+urllib.parse.quote('titles.title:"law of the iterated logarithm for tail sums" AND creators.name:Ghimire')+'&page[size]=8'),
('crossref_conditional2016.json','https://api.crossref.org/works/10.3126%2Fjacem.v2i0.16100'),
('inequalities2020.pdf','https://thescipub.com/pdf/jmssp.2020.233.238.pdf'),
('survey2022.pdf','https://www.nepjol.info/index.php/JIST/article/view/45505/34119'),
]
receipts=[]
for name,url in sources:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior audit PR1292 (read-only primary-source metadata)'}),timeout=30) as r:
   b=r.read(1600001)
   if len(b)>1600000:raise RuntimeError('bounded identity read exceeded 1.6MB')
   (P/'sources'/name).write_bytes(b)
   rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:rec.update(status=getattr(e,'code',None),error=repr(e))
 receipts.append(rec);(P/'IDENTITY_FETCH_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.3)
for name in ['inequalities2020.pdf','survey2022.pdf']:
 f=P/'sources'/name
 if f.exists() and f.read_bytes().startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
