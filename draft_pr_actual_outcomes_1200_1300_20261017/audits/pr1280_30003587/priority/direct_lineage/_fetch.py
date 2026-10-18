from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,datetime,json,hashlib,subprocess
BASE=Path('.')
urls={
 'bs_v1':'https://arxiv.org/pdf/1708.08258v1',
 'bs_v2':'https://arxiv.org/pdf/1708.08258v2',
 'bs_v3':'https://arxiv.org/pdf/1708.08258v3',
 'bs_final_old':'https://www.mscand.dk/article/download/114823/164463/240286',
 'bs_final_new':'https://journals.msp.org/mscand/article/download/221/220',
 'owr':'https://ems.press/content/serial-article-files/46706',
 'cartan_ii':'https://link.springer.com/content/pdf/10.1007/s00208-020-02022-4.pdf',
 'izumi_index':'https://www.math.kyoto-u.ac.jp/preprint/preprint2002.html',
 'owr_doi':'https://doi.org/10.4171/OWR/2017/42',
 'bs_abs':'https://arxiv.org/abs/1708.08258',
 'bs_publisher':'https://journals.msp.org/mscand/article/view/221',
 'szabo_publications':'https://gaborszabo.nfshost.com/publications.html',
}
def get(item):
 k,u=item; m={'id':k,'requested_url':u,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Independent mathematical literature audit; Python urllib'}),timeout=45) as r:
   b=r.read();m.update(final_url=r.url,status=r.status,content_type=r.headers.get('content-type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  suffix='.pdf' if b.startswith(b'%PDF') else '.html'
  p=BASE/'_local'/('raw_pdfs' if suffix=='.pdf' else 'provider_responses')/(k+suffix);p.write_bytes(b);m['private_path']=str(p)
  if suffix=='.pdf':
   subprocess.run(['pdftotext','-layout',str(p),str(BASE/'_local'/'extracts'/(k+'.txt'))],check=True)
 except Exception as e:m['error']=str(e)
 m['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();return m
results=list(ThreadPoolExecutor(8).map(get,urls.items()))
(BASE/'_local'/'retrievals_initial.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
