from pathlib import Path
import urllib.request,json,hashlib,datetime,subprocess
p=Path(__file__).resolve().parent
urls=[('circle_ci.pdf','https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf',700000),('tao_note.pdf','https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf',500000),('wang_proposal.pdf','https://multiscalar.ai/results/erdos-1038/paper.pdf',700000),('ehp1958.pdf','https://users.renyi.hu/~p_erdos/1958-05.pdf',4500000),('modern_ep1038.html','https://www.erdosproblems.com/1038',160000),('wang_status.html','https://multiscalar.ai/results/erdos-1038/',120000)]
rs=[]
for name,url,cap in urls:
 rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent analytic original-scope audit PR1310 (read-only primary source)'}),timeout=25)as r:
   b=r.read(cap+1)
   if len(b)>cap:raise RuntimeError('bounded source read limit exceeded')
   (p/'sources'/name).write_bytes(b);rec.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),content_type=r.headers.get('Content-Type'),pdf_signature=b.startswith(b'%PDF-'))
   if b.startswith(b'%PDF-') and name!='ehp1958.pdf':subprocess.run(['pdftotext','-layout',str(p/'sources'/name),str((p/'sources'/name).with_suffix('.txt'))],check=True)
 except Exception as e:rec.update(status=getattr(e,'code',None),error=repr(e))
 rs.append(rec);(p/'SOURCE_FETCH_RECEIPTS.json').write_text(json.dumps(rs,indent=2)+'\n');print(name,rec.get('status'),rec.get('bytes'),rec.get('error'),flush=True)
