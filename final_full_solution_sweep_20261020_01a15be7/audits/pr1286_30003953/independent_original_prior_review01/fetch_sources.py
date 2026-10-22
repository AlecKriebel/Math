from pathlib import Path
import json,urllib.request,hashlib,time,datetime,subprocess
P=Path(__file__).resolve().parent
urls=[('original_owr2018.pdf','https://ems.press/content/serial-article-files/46762'),('psw_published.pdf','https://msp.org/gt/2023/27-8/gt-v27-n8-p06-s.pdf'),('gm_arxiv_v2.pdf','https://arxiv.org/pdf/1809.10639v2'),('psw_version_doi.html','https://doi.org/10.2140/gt.2023.27.3303'),('crossref_psw.json','https://api.crossref.org/works/10.2140%2Fgt.2023.27.3303'),('crossref_gm.json','https://api.crossref.org/works/10.4310%2FMRL.241024233904'),('crossref_original.json','https://api.crossref.org/works/10.4171%2FOWR%2F2018%2F40'),('gm_version_doi.html','https://doi.org/10.4310/MRL.241024233904'),('psw_arxiv_metadata.json','https://api.datacite.org/dois/10.48550/arxiv.1910.06627'),('gm_arxiv_metadata.json','https://api.datacite.org/dois/10.48550/arxiv.1809.10639'),('gm_author_publications.html','https://www.imo.universite-paris-saclay.fr/~daniel.monclair/research.html')]
rs=[]
for name,url in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior review PR1286 (read-only)'})
  with urllib.request.urlopen(req,timeout=40)as r:
   b=r.read(8*1024*1024+1)
   if len(b)>8*1024*1024:raise RuntimeError('size guard')
   with(P/'sources'/name).open('xb')as h:h.write(b)
   rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_signature=b.startswith(b'%PDF-'))
 except Exception as e:rec.update(error=str(e),error_type=type(e).__name__,status=getattr(e,'code',None))
 rs.append(rec);(P/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.5)
for name in ['original_owr2018','psw_published','gm_arxiv_v2']:
 f=P/'sources'/(name+'.pdf')
 if f.exists()and f.read_bytes().startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
