from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
p=Path(__file__).resolve().parent/'primary-sources'
urls=[('englander-v4','https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4.full.pdf'),('huber-quarnets','https://ueaeprints.uea.ac.uk/id/eprint/99242/7/Huber_etal_2025_BullMathBiol.pdf'),('brits-v3','https://arxiv.org/pdf/2607.12919v3')]
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  r=urllib.request.urlopen(req,timeout=45);data=r.read()
  z={'name':name,'url':url,'resolved_url':r.url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf':data.startswith(b'%PDF')}
  if z['pdf']:(p/(name+'.pdf')).write_bytes(data)
  else:z['error']='response is not PDF'
 except Exception as e:z={'name':name,'url':url,'error':repr(e)}
 print(z,flush=True);return z
results=list(concurrent.futures.ThreadPoolExecutor(3).map(fetch,urls));(p/'receipt.json').write_text(json.dumps(results,indent=2)+'\n')
