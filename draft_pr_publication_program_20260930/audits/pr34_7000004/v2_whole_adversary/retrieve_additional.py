from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
H=Path(__file__).resolve().parent;D=H/'tmp/primary_sources';D.mkdir(exist_ok=True)
items=[('author-asymptotic.pdf','https://ghomi.math.gatech.edu/Papers/asymptotic.pdf','669823c1ce5db7b1d3a6fa4f7382ede672cf7a9e9f017ffe5a52b869fab4544b'),('h-principle.pdf','https://arxiv.org/pdf/2510.05275v1','6ade0d9b954d5b8b593818b3027d32437d011784fdfe4def7227c1669d9b4623'),('banchoff.html','https://www.math.brown.edu/tbanchof/balt/ma106/dtext41.html','d2c8f4693cbf7891d20ba3d4353f41583a2a55b0a582481cc26e839fc3f3e330'),('kovaleva.pdf','https://www.mathnet.ru/php/getFT.phtml?jrnid=fpm&paperid=115&what=fullt','f0b7e98dd1a8bcb237303572f4a4089d337557f70355e7e4fd656dff734f8691')]
def get(z):
 name,url,want=z;o={'name':name,'requested_url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as f:b=f.read();o.update(final_url=f.url,status=f.status,last_modified=f.headers.get('Last-Modified'))
  (D/name).write_bytes(b);o.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),matches_previous_primary=hashlib.sha256(b).hexdigest()==want)
 except Exception as e:o['error']=repr(e)
 return o
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:o=list(p.map(get,items))
(H/'ADDITIONAL_SOURCE_RETRIEVALS.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
