"""GET-only public source-family discovery; retains errors and complete stream hashes."""
from pathlib import Path
import json,types,sys,datetime,gzip,hashlib,concurrent.futures
O=Path(__file__).resolve().parent;mods={}
for n in ['ops_core','authority','providers']:
 p=O/'source'/(n+'.py');m=types.ModuleType(n);m.__file__=str(p);sys.modules[n]=m;exec(compile(p.read_bytes(),str(p),'exec',optimize=0),m.__dict__);mods[n]=m
cfg=json.loads((O/'RUNTIME_CONFIGURATION.json').read_bytes());requests=json.loads((O/'PUBLIC_REQUESTS_DISCOVERY.json').read_bytes())['requests'];cap=mods['providers'].Capture(O/'private/public_initial_reads');provider=mods['providers'].RealProvider(cfg,{},cap,lambda:None);results={};errors=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 fs={pool.submit(provider.public_one,r):r for r in requests}
 for f in concurrent.futures.as_completed(fs):
  r=fs[f]
  try:results[r['key']]=f.result()
  except Exception as e:errors.append({'key':r['key'],'url':r['url'],'error_type':type(e).__name__,'error':str(e)});cap.save('FAILED_PUBLIC_GET',errors[-1])
b=(json.dumps({'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'errors':errors,'action_authority':False},sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();z=gzip.compress(b,mtime=0);(O/'private/PUBLIC_INITIAL_COMPLETE.json.gz').write_bytes(z);print(json.dumps({'results':len(results),'status_counts':{str(n):sum(x['status']==n for x in results.values())for n in set(x['status']for x in results.values())},'errors':errors,'raw_sha256':hashlib.sha256(b).hexdigest(),'gzip_bytes':len(z)}))
