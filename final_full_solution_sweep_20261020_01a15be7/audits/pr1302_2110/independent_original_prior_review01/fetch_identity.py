from pathlib import Path
import urllib.request,urllib.parse,json,datetime,hashlib,subprocess,time
p=Path(__file__).resolve().parent
items=[('arxiv_abs.html','https://arxiv.org/abs/2609.17543',120000),('arxiv_v1.pdf','https://arxiv.org/pdf/2609.17543v1',250000),('datacite_prior.json','https://api.datacite.org/dois/10.48550/arxiv.2609.17543',100000),('doi_prior_response.bin','https://doi.org/10.48550/arXiv.2609.17543',150000),('crossref_ccdn.json','https://api.crossref.org/works/10.2140%2Fant.2020.14.2261',100000),('crossref_jia.json','https://api.crossref.org/works/10.4064%2Faa-76-1-21-84',30000),('crossref_title_query.json','https://api.crossref.org/works?query.title='+urllib.parse.quote('Distinct Consecutive Products')+'&query.author=Chojecki&rows=8',150000)]
rs=[]
for name,url,cap in items:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior audit PR1302 (read-only publication identity)'}),timeout=25) as r:
   b=r.read(cap+1)
   if len(b)>cap:raise RuntimeError('bounded identity read exceeded cap')
   (p/'sources'/name).write_bytes(b);rec.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),content_type=r.headers.get('Content-Type'))
   if b.startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(p/'sources'/name),str((p/'sources'/name).with_suffix('.txt'))],check=True)
 except Exception as e:rec.update(status=getattr(e,'code',None),error=repr(e))
 rs.append(rec);(p/'IDENTITY_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.3)
