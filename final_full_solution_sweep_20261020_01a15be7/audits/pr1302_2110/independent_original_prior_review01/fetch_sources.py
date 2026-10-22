from pathlib import Path
import urllib.request,json,datetime,hashlib,subprocess,time
P=Path(__file__).resolve().parent
urls=[('chojecki2026.pdf','https://ulam.ai/research/erdos421-sol.pdf',300000),('jia1996.pdf','https://matwbn.icm.edu.pl/ksiazki/aa/aa76/aa7613.pdf',600000),('ccdn2020.pdf','https://msp.org/ant/2020/14-8/ant-v14-n8-p09-s.pdf',1800000),('erdos_graham1980.pdf','https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf',5500000),('modern_ep421.html','https://www.erdosproblems.com/421',300000)]
rs=[]
for name,url,cap in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical original/prior audit PR1302 (read-only primary source verification)'}),timeout=30) as r:
   b=r.read(cap+1)
   if len(b)>cap:raise RuntimeError('bounded source read exceeded cap')
   (P/'sources'/name).write_bytes(b);rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_signature=b.startswith(b'%PDF-'))
   if b.startswith(b'%PDF-'):subprocess.run(['pdftotext','-layout',str(P/'sources'/name),str((P/'sources'/name).with_suffix('.txt'))],check=True)
 except Exception as e:rec.update(status=getattr(e,'code',None),error=repr(e))
 rs.append(rec);(P/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True);time.sleep(.2)
