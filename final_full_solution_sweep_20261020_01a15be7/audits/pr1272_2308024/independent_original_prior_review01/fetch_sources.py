from pathlib import Path
import urllib.request,urllib.error,json,hashlib,time,datetime
P=Path(__file__).resolve().parent
SOURCES={
'original_2018v2.pdf':'https://arxiv.org/pdf/1809.07200v2',
'abtahi_honary_2007.pdf':'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0F35F1AEC3DABCA443679F53A750214A/S0017089507003576a.pdf/properties_of_certain_subalgebras_of_dalesdavie_algebras.pdf',
'feinstein_kamowitz.pdf':'https://www.maths.nottingham.ac.uk/plp/pmzjff/Papers/pdf/FK4.pdf',
'dales_davie_1973_publisher.html':'https://www.sciencedirect.com/science/article/pii/0022123673900657',
'dales_davie_1973.pdf':'https://www.sciencedirect.com/science/article/pii/0022123673900657/pdf',
'original_2019_chapter.html':'https://link.springer.com/chapter/10.1007/978-3-030-25165-9_8',
'original_2019_chapter.pdf':'https://link.springer.com/content/pdf/10.1007/978-3-030-25165-9_8.pdf',
'crossref_dales_davie.json':'https://api.crossref.org/works/10.1016%2F0022-1236(73)90065-7',
'crossref_abtahi_honary.json':'https://api.crossref.org/works/10.1017%2FS0017089507003576',
'crossref_original_2019.json':'https://api.crossref.org/works/10.1007%2F978-3-030-25165-9_8',
'original_2018_abstract.html':'https://arxiv.org/abs/1809.07200v2'}
receipts=[]
for name,url in SOURCES.items():
 out=P/'sources'/name
 if out.exists():raise RuntimeError('do not overwrite existing capture '+name)
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source audit PR1272 (read-only; no automated publication)'})
  with urllib.request.urlopen(req,timeout=35) as r:
   b=r.read(8*1024*1024+1)
   if len(b)>8*1024*1024:raise RuntimeError('source size guard')
   rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
   out.write_bytes(b)
 except Exception as e:
  rec.update(error_type=type(e).__name__,error=str(e),status=getattr(e,'code',None))
 receipts.append(rec)
 (P/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True)
 time.sleep(.5)
