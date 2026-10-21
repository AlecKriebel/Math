#!/usr/bin/env python3
import pathlib,json,urllib.request,re,hashlib,datetime,subprocess,concurrent.futures,html
W=pathlib.Path(__file__).resolve().parent
urls={883:'https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf',885:'https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html',888:'https://ems.press/content/serial-article-files/46955',894:'https://ems.press/content/serial-article-files/48175',904:'https://ems.press/journals/owr/articles/1111',905:'https://ems.press/journals/owr/articles/1465'}
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:return r.read(),r.url,dict(r.headers)
def one(n):
 p=W/'downloads_private'/str(n);u=urls[n];b,fu,headers=get(u);meta={'pr':n,'url':u,'final_url':fu,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if n in (904,905):
  (p/'problem_page.html').write_bytes(b);t=b.decode();links=re.findall(r'(?:https://ems.press)?(/content/serial-article-files/\d+)',t);meta['pdf_discovered_links']=list(dict.fromkeys(links));u='https://ems.press'+links[0];b,fu,headers=get(u);meta['pdf_url']=u;meta['pdf_final_url']=fu
 meta['bytes']=len(b);meta['sha256']=hashlib.sha256(b).hexdigest()
 if b.startswith(b'%PDF-'):
  f=p/'original_problem.pdf';f.write_bytes(b);subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
 else:(p/'original_problem.html').write_bytes(b)
 return meta
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:out=list(e.map(one,urls))
(W/'PROBLEM_SOURCE_FETCH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
