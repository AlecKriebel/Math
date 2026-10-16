from pathlib import Path
import urllib.request,datetime,json,hashlib,concurrent.futures,subprocess,sys
P=Path(__file__).resolve().parent
items=json.loads(sys.argv[1])
def get(it):
 key,url=it; r={'id':key,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=55) as response:
   b=response.read(); r.update(final_url=response.url,status=response.status,content_type=response.headers.get('Content-Type'))
  ext='pdf' if b.startswith(b'%PDF') else 'html';f=P/'private'/f'{key}.{ext}';f.write_bytes(b);f.chmod(0o600)
  r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),private_file=f.name)
  if ext=='pdf':
   target=f.with_suffix('.txt');z=subprocess.run(['pdftotext','-layout',str(f),str(target)],capture_output=True,text=True);r['extract_exit']=z.returncode
   if target.exists():target.chmod(0o600)
 except Exception as e:r['error']=repr(e)
 return r
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(get,items))
f=P/'RETRIEVALS.json';r=json.loads(f.read_text()) if f.exists() else [];r.extend(results);f.write_text(json.dumps(r,indent=2)+'\n')
for item in results:print(item)
