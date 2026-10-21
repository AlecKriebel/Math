from pathlib import Path
import concurrent.futures,datetime as dt,hashlib,json,subprocess,urllib.request
HERE=Path(__file__).resolve().parent
EFFORT=HERE.parents[3]
PRIVATE=EFFORT/'private/pr0399_priority'
SOURCES=[
 ('skeide_index2006','https://arxiv.org/pdf/math/0601228'),
 ('skeide_sigma2022','https://www.emis.de/journals/SIGMA/2022/071/sigma22-071.pdf'),
 ('fowler1995','https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2C3A014CE77433BD194B5F9FC1235043/S0008414X00046411a.pdf/free_e_0semigroups.pdf'),
 ('tsirelson2004','https://arxiv.org/pdf/math/0402431'),
 ('liebscher_randomsets','https://arxiv.org/pdf/math/0306365'),
 ('shalit_skeide2020','https://arxiv.org/pdf/2003.05166'),
 ('skeide_classification2016','https://arxiv.org/pdf/0901.1798'),
 ('skeide_abstract2013','https://iris.unimol.it/handle/11695/17119'),
 ('skeide_abstract2016','https://www.math.uni.wroc.pl/analiza/bedlewo17/abstracts.pdf'),
 ('skeide_roland65','https://www.uni-saarland.de/fileadmin/upload/lehrstuhl/weber-moritz/Roland65/R65titles_and_abstracts.pdf'),
 ('skeide_seminar2026','https://www.uni-saarland.de/fr/lehrstuhl/weber-moritz/research/research-seminar-noncommutative-and-functional-analysis.html'),
]
def fetch(item):
 name,url=item;now=dt.datetime.now(dt.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent mathematical source audit)'})
  with urllib.request.urlopen(req,timeout=40) as r:data=r.read();resolved=r.url
  pdf=data.startswith(b'%PDF');path=PRIVATE/(name+('.pdf' if pdf else '.html'));path.write_bytes(data)
  rec={'name':name,'requested_url':url,'resolved_url':resolved,'retrieved_utc':now,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'format':'pdf' if pdf else 'html','private_path':path.relative_to(EFFORT).as_posix(),'reading_scope':'pending'}
  if pdf:
   textpath=path.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(path),str(textpath)],check=True,capture_output=True);b=textpath.read_bytes();rec['text_sha256']=hashlib.sha256(b).hexdigest()
  return rec
 except Exception as e:return {'name':name,'requested_url':url,'retrieved_utc':now,'error':str(e),'reading_scope':'unrecovered'}
if __name__=='__main__':
 PRIVATE.mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:receipts=list(pool.map(fetch,SOURCES))
 (HERE/'SOURCE_DOWNLOADS.json').write_text(json.dumps({'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'Source custody only; reading scopes are independently specified elsewhere. Full bodies remain ignored private.','sources':receipts},indent=2)+'\n')
 print(json.dumps([{'name':x['name'],'bytes':x.get('bytes'),'error':x.get('error')} for x in receipts],indent=2))
