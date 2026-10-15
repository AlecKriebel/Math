from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess,concurrent.futures
HERE=Path(__file__).resolve().parent
sources={
'owr':'https://ems.press/content/serial-article-files/46100',
'laurent2010':'https://homepages.cwi.nl/~monique/files/moment-ima-update-new.pdf',
'laurent2009published':'https://homepages.cwi.nl/~monique/files/moment-ima.pdf',
'reznick2000':'https://reznick.web.illinois.edu/Paper34.pdf',
'tentacle':'https://www.math.uni-konstanz.de/~schweigh/publications/tentacle.pdf',
'gcv':'https://perso.lip6.fr/Mohab.Safey/Articles/gcv_sos.pdf'}
def fetch(item):
 key,url=item
 req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
 with urllib.request.urlopen(req,timeout=60) as response:
  b=response.read();resolved=response.url;ct=response.headers.get('Content-Type')
 if not b.startswith(b'%PDF'): raise RuntimeError('Not PDF '+key)
 p=HERE/'private_sources'/f'{key}.pdf';p.write_bytes(b)
 subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True,capture_output=True)
 info=subprocess.run(['pdfinfo',str(p)],check=True,text=True,capture_output=True).stdout
 return {'key':key,'url':url,'resolved_url':resolved,'content_type':ct,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pdfinfo':info,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_redistributed':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: records=list(pool.map(fetch,sources.items()))
(HERE/'evidence/fresh_source_hashes.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ('key','bytes','sha256')} for r in records],indent=2))
