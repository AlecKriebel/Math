from pathlib import Path
import urllib.request,json,hashlib,datetime,concurrent.futures,subprocess
R=Path(__file__).resolve().parent
S=R/'sources';D=S/'raw';D.mkdir(parents=True,exist_ok=True)
(S/'.gitignore').write_text('raw/\n')
P=R.parent.parent/'publication/evidence/priority_review_01/sources/SOURCE_PINS.json'
sources=json.loads(P.read_text())['sources']
ids={'owr2015','harvey_lawson1982','fawzi2021','fawzi2019v1','orbitopes2011','theta_gpt2010','rostalski2010slides','theta_bookchapter2013','curvature2021v2','bsv2016_arxiv','gpt_lifts2013','lifting_simplicity2022','vrana_levay2009','grabowski_kus_marmo2012','barvinok_blekherman2005'}
def fetch(s):
 r={'id':s['id'],'url':s['url'],'version_from_published_ledger':s.get('version'),'locators_from_published_ledger':s.get('locators'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=45) as f:
   b=f.read();r.update(final_url=f.url,content_type=f.headers.get('Content-Type'))
  r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),matches_prior_bytes=hashlib.sha256(b).hexdigest()==s.get('sha256'))
  if not b.startswith(b'%PDF'):raise ValueError('not PDF')
  p=D/(s['id']+'.pdf');p.write_bytes(b)
  t=D/(s['id']+'.txt');q=subprocess.run(['pdftotext','-layout',str(p),str(t)],capture_output=True)
  r.update(text_extract_exit=q.returncode,text_extract_stderr=q.stderr.decode(),path='raw/'+p.name,status='retrieved')
 except Exception as e:r.update(status='failed',error=str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(fetch,[s for s in sources if s['id'] in ids]))
(S/'SOURCE_FETCH_RECEIPT.json').write_text(json.dumps({'sources':results,'raw_policy':'Third-party source bodies remain only in package_03/sources/raw and are not public-package modifications.'},indent=2)+'\n')
print(json.dumps([{k:r.get(k) for k in ['id','status','bytes','sha256','matches_prior_bytes','error']} for r in results],indent=2))
