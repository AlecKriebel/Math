from pathlib import Path
import urllib.request,urllib.error,json,hashlib,datetime,time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');S=P/'papers/23124601/sources'; E=P/'papers/23124601/reviews/scope'
receipts=[]
def get(url,name):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();p=S/name
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification; ordinary public HTTPS'})
  with urllib.request.urlopen(req,timeout=25) as r:
   b=r.read(100*1024*1024+1)
   if len(b)>100*1024*1024:raise ValueError('100MiB bounded fetch exceeded')
   row={'requested_url':url,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'method':'GET','status':r.status,'reason':r.reason,'final_url':r.url,'headers_in_original_order':list(r.headers.raw_items()),'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()}
  with p.open('xb') as out:out.write(b)
 except Exception as ex:
  row={'requested_url':url,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET','error':repr(ex)}
  receipts.append(row);(S/'transport-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');raise
 receipts.append(row);(S/'transport-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');return b
body=get('https://zenodo.org/api/records/23124601','record.raw.json');j=json.loads(body)
print(json.dumps({'id':j.get('id'),'metadata':j.get('metadata'),'links':j.get('links'),'files':j.get('files')},indent=2),flush=True)
for key,name in [('latest','latest.raw.json'),('versions','versions.raw.json')]:
 u=j['links'].get(key)
 if not u:raise ValueError('missing native '+key+' link')
 get(u,name)
for f in j['files']:
 key=f['key'];assert key==Path(key).name and key not in {'.','..'}
 b=get(f['links']['self'],key)
 assert len(b)==f['size'],('size',key)
 assert f['checksum'].lower()=='md5:'+hashlib.md5(b).hexdigest(),('MD5',key)
print('ALL_NATIVE_ASSETS_FETCHED',flush=True)
