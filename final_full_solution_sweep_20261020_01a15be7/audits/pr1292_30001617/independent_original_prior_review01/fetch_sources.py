from pathlib import Path
import urllib.request,json,hashlib,datetime,time,subprocess
P=Path(__file__).resolve().parent
urls=[('original_owr2010.pdf','https://ems.press/content/serial-article-files/46308'),('ghimire_thesis2012.pdf','https://krex.k-state.edu/bitstreams/988fff3e-b27c-42e4-b215-308672e268fa/download'),('ghimire_talk2011.pdf','https://www.math.ksu.edu/about/events/conference/pas/2011/talks/Prairie%20Analysis%20pause.pdf'),('conditional2016.pdf','https://www.nepjol.info/index.php/JACEM/article/view/16100/13051'),('thesis_handle.html','https://hdl.handle.net/2097/13647'),('original_doi.html','https://doi.org/10.4171/OWR/2010/49'),('crossref_original.json','https://api.crossref.org/works/10.4171%2FOWR%2F2010%2F49'),('conditional2016_landing.html','https://www.nepjol.info/index.php/JACEM/article/view/16100')]
rs=[]
for name,url in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior audit PR1292 (read-only)'}),timeout=40)as r:
   b=r.read(3*1024*1024+1)
   if len(b)>3*1024*1024:raise RuntimeError('source size budget')
   with(P/'sources'/name).open('xb')as h:h.write(b)
   rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_signature=b.startswith(b'%PDF-'))
 except Exception as e:rec.update(error=str(e),error_type=type(e).__name__,status=getattr(e,'code',None))
 rs.append(rec);(P/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.5)
for name in ['original_owr2010','ghimire_thesis2012','ghimire_talk2011','conditional2016']:
 f=P/'sources'/(name+'.pdf')
 if f.exists()and f.read_bytes().startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
