from pathlib import Path
import urllib.request,json,hashlib,datetime,time
P=Path(__file__).resolve().parent
urls=[('original_owr2017.pdf','https://ems.press/content/serial-article-files/46673'),('zenodo_record_live.json','https://zenodo.org/api/records/23107180'),('zenodo_versions.json','https://zenodo.org/api/records/23107180/versions'),('version_doi.html','https://doi.org/10.5281/zenodo.23107180'),('concept_doi.html','https://doi.org/10.5281/zenodo.23107179'),('datacite_version.json','https://api.datacite.org/dois/10.5281/zenodo.23107180'),('datacite_concept.json','https://api.datacite.org/dois/10.5281/zenodo.23107179'),('crossref_original.json','https://api.crossref.org/works/10.4171%2FOWR%2F2017%2F7'),('prior_landing.html','https://eulersolve.org/papers/owr-15212-005/')]
rs=[]
for name,url in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  q=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source audit PR1276 (read-only)'})
  with urllib.request.urlopen(q,timeout=40) as r:
   d=r.read(9*1024*1024+1)
   if len(d)>9*1024*1024:raise RuntimeError('size guard')
   with(P/'sources'/name).open('xb') as f:f.write(d)
   rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(d),sha256=hashlib.sha256(d).hexdigest(),pdf_signature=d.startswith(b'%PDF-'))
 except Exception as e:rec.update(error_type=type(e).__name__,error=str(e),status=getattr(e,'code',None))
 rs.append(rec);(P/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.5)
