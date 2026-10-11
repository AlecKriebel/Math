from pathlib import Path
import concurrent.futures, urllib.request, hashlib, json, datetime, subprocess
ROOT=Path(__file__).resolve().parent
SOURCES={
'bandeira2013.html':'https://afonsobandeira.wordpress.com/2013/11/01/a-conjecture-on-the-singular-values-of-a-gaussian-matrix/',
'mit2015.pdf':'https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/a9963e8f7bd9c10b4d48df8115f63116_MIT18_S096F15_Open1.2.pdf',
'real_v2.pdf':'https://arxiv.org/pdf/2608.12151v2',
'complex_v2.pdf':'https://arxiv.org/pdf/2608.12147v2',
'bd_v1.pdf':'https://arxiv.org/pdf/2608.27532v1',
'ap_v1.pdf':'https://arxiv.org/pdf/2609.07802v1',
'real_v2_abs.html':'https://arxiv.org/abs/2608.12151v2',
'complex_v2_abs.html':'https://arxiv.org/abs/2608.12147v2',
'bd_v1_abs.html':'https://arxiv.org/abs/2608.27532v1',
'ap_v1_abs.html':'https://arxiv.org/abs/2609.07802v1',
'withdrawn_v3_abs.html':'https://arxiv.org/abs/1606.00494v3',
'livan_vivo_v2.pdf':'https://arxiv.org/pdf/1105.??'}
del SOURCES['livan_vivo_v2.pdf']
def fetch(item):
 name,url=item; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(request,timeout=60) as resp: data=resp.read(); final=resp.url; status=resp.status
  path=ROOT/'tmp/sources'/name; path.write_bytes(data)
  record={'name':name,'url':url,'final_url':final,'utc':start,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':status}
  if name.endswith('.pdf'):
   target=path.with_suffix('.txt'); p=subprocess.run(['pdftotext','-layout',str(path),str(target)],capture_output=True,text=True)
   record['extraction_returncode']=p.returncode; record['text_sha256']=hashlib.sha256(target.read_bytes()).hexdigest() if p.returncode==0 else None
  return record
 except Exception as e: return {'name':name,'url':url,'utc':start,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: records=list(ex.map(fetch,SOURCES.items()))
(ROOT/'SOURCE_RECEIPTS.json').write_text(json.dumps({'purpose':'Fresh primary retrieval before historical report exposure','sources':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
