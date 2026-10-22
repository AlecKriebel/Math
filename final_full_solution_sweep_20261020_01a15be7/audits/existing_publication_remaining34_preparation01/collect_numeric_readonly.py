"""Fresh CLI GETs only. No account-token access, auth change or mutation provider."""
from pathlib import Path
import types,sys,subprocess,json,gzip,hashlib,datetime,os
O=Path(__file__).resolve().parent
for name in ['ops_core','numeric']:
 p=O/'source'/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(p.read_bytes(),str(p),'exec',optimize=0),m.__dict__)
class GetOnly:
 def __init__(self):self.raw=[]
 def gws(self,parts,params,body=None):
  if parts not in [['get'],['values','batchGetByDataFilter']]:raise RuntimeError('GET-only')
  command=['gws','sheets','spreadsheets',*parts,'--params',json.dumps(params)]
  if body is not None:command+=['--json',json.dumps(body)]
  r=subprocess.run(command,capture_output=True)
  if r.returncode:raise RuntimeError('GWS GET failed; no credential/body printed')
  name='numeric_raw'+str(len(self.raw));raw=r.stdout;self.raw.append({'name':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)});(O/'private'/(name+'.json.gz')).write_bytes(gzip.compress(raw,mtime=0));return sys.modules['ops_core'].strict_json(raw)
p=GetOnly();start=datetime.datetime.now(datetime.timezone.utc).isoformat();v=sys.modules['numeric'].observe(p);raw=(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();(O/'private/numeric_complete.json.gz').write_bytes(gzip.compress(raw,mtime=0));out={'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':len(v['values']),'all43typed_dual_raw_full_metadata':True,'numeric_gid':1254632077,'raw':p.raw,'action_readiness':False};(O/'NUMERIC_DATED_OBSERVATION.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out))
