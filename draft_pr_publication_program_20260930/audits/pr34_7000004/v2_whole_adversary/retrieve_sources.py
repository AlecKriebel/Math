from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
H=Path(__file__).resolve().parent;D=H/'tmp/primary_sources';D.mkdir(parents=True,exist_ok=True)
items=[('ghomi-op.pdf','https://people.math.gatech.edu/~ghomi/Papers/op.pdf','6ff7c016b904e2a606afe8fff1f88522f15b8e8528795e74eee56ece537e264e'),('ni-v1.pdf','https://arxiv.org/pdf/2606.29231v1','0ec8ff7da6224ece69f2beee6e71a39697a2fbc4a0aacb01b384755e69f9bbd2'),('asymptotic-v2.pdf','https://arxiv.org/pdf/2412.19266v2','1329d83437393ff0cf984466a28fc6cf384e8e5b1e38f1ef2a9fcb868e61489a'),('Asymptotic-Examples.nb','https://ghomi.math.gatech.edu/MathematicaNBs/Asymptotic-Examples.nb','89791fab271dacd16351bd21c1162c02ecbe26ee506a0dbffd8d76cda03fbd5d')]
def get(z):
 name,url,want=z;r={'name':name,'url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as f:b=f.read();r.update(final_url=f.url,http_status=f.status)
  (D/name).write_bytes(b);r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),matches_frozen_primary=hashlib.sha256(b).hexdigest()==want)
 except Exception as e:r.update(error=type(e).__name__+': '+str(e),matches_frozen_primary=False)
 r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(get,items))
(H/'SOURCE_RETRIEVALS.json').write_text(json.dumps({'sources':r,'scope':'Read-only primary retrieval, no outside-person outreach. Files are ignored primary inputs, not authored audit artifacts.'},indent=2)+'\n')
print(json.dumps(r,indent=2))
