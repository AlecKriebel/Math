from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess,sys
ROOT=Path(__file__).resolve().parent
name,url=sys.argv[1:3]
meta={'name':name,'requested_url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-Math-Priority-Audit/1.0'})
 with urllib.request.urlopen(req,timeout=35) as r:
  data=r.read();meta.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
 dest=ROOT/'sources/private'/name; dest.write_bytes(data)
 meta.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),private_body=str(dest.relative_to(ROOT)))
 if data.startswith(b'%PDF'):
  subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True)
except Exception as ex:meta.update(error=type(ex).__name__+': '+str(ex))
p=ROOT/'SOURCE_FETCH.json'
rows=json.loads(p.read_text()) if p.exists() else []
rows.append(meta);p.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(meta))
