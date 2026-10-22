"""Fresh numeric43 typed raw CLI GET collection; exact duplicate bytes reused."""
from pathlib import Path
import types,sys,json,gzip,hashlib,subprocess,datetime,os
O=Path(__file__).resolve().parent
for name in['ops_core','numeric']:
 p=O/'source'/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(p.read_bytes(),str(p),'exec',optimize=0),m.__dict__)
cache={}
for p in(O/'private').glob('numeric*.json.gz'):
 b=gzip.decompress(p.read_bytes());cache[hashlib.sha256(b).hexdigest()]=p
pins=[]
def save(label,b):
 h=hashlib.sha256(b).hexdigest();p=cache.get(h)
 if p is not None:assert gzip.decompress(p.read_bytes())==b;reused=True
 else:
  p=O/'private'/(label+'.json.gz');assert not p.exists();z=gzip.compress(b,mtime=0);assert sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')])+len(z)+4096<10*1024*1024;assert os.statvfs(O).f_bavail*os.statvfs(O).f_frsize-len(z)>150*1024*1024;p.write_bytes(z);cache[h]=p;reused=False
 return {'path':str(p.relative_to(O)),'raw_sha256':h,'raw_bytes':len(b),'fresh_response_reuses_identical_retained_bytes':reused}
class GetOnly:
 def gws(self,parts,params,body=None):
  assert parts in[['get'],['values','batchGetByDataFilter']];command=['gws','sheets','spreadsheets',*parts,'--params',json.dumps(params)]
  if body is not None:command+=['--json',json.dumps(body)]
  r=subprocess.run(command,capture_output=True)
  if r.returncode:raise RuntimeError('GWS GET failed; no body/credential printed')
  pins.append(save('closing_numeric_raw'+str(len(pins)),r.stdout));return sys.modules['ops_core'].strict_json(r.stdout)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();v=sys.modules['numeric'].observe(GetOnly());capture=save('closing_numeric_complete',(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode());before=json.loads(gzip.decompress((O/'private/numeric_complete.json.gz').read_bytes()));old=len(before['values']);assert sys.modules['ops_core'].typed_equal(v['values'][:old],before['values']);out={'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'numeric_gid':1254632077,'all43_full_raw_typed_VALUE_FORMULA_complete_metadata':True,'rows':len(v['values']),'old237_rows_exact_typed_preserved':True,'fresh_raw':pins,'complete_observation':capture,'new_full_rows':[{'row_number':i,'full43_cells':row}for i,row in enumerate(v['values'][old:],old+1)],'dated_only_not_action_lock':True,'action_authority':False};(O/'CLOSING_NUMERIC_DATED_OBSERVATION.json').write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in['fresh_raw','new_full_rows']}));print(json.dumps(out['new_full_rows'],ensure_ascii=False))
