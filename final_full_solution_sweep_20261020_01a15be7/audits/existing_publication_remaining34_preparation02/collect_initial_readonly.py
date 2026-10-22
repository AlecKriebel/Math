"""Current CLI/account/local collection. GET-only; no production CASE/authority."""
from pathlib import Path
import json,gzip,hashlib,subprocess,types,sys,datetime,os
O=Path(__file__).resolve().parent
pins=json.loads((O/'SOURCE_READ_CLIENT_PINS.json').read_bytes());mods={}
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
cache={};captures=[]
def save(label,b):
 h=sha(b)
 if h not in cache:
  p=O/'private'/(label+'.json.gz');assert not p.exists();z=gzip.compress(b,mtime=0);assert sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')])+len(z)+4096<10*1024*1024;assert os.statvfs(O).f_bavail*os.statvfs(O).f_frsize-len(z)>150*1024*1024;p.write_bytes(z);cache[h]=p
 return {'path':str(cache[h].relative_to(O)),'bytes':len(b),'sha256':h}
for name in ['ops_core','numeric','providers']:
 q=Path(pins[name+'.py']['source']);b=q.read_bytes();assert sha(b)==pins[name+'.py']['sha256'];m=types.ModuleType(name);m.__file__=str(q);sys.modules[name]=m;exec(compile(b,str(q),'exec',optimize=0),m.__dict__);mods[name]=m
C=mods['ops_core']
class GetOnly(mods['providers'].RealProvider):
 def run(self,command,capture_output=True):
  assert command[:4]==['gws','sheets','spreadsheets','get']or command[:5]==['gws','sheets','spreadsheets','values','batchGetByDataFilter'];r=subprocess.run(command,capture_output=True);captures.append({'command':command,'returncode':r.returncode,'stdout':save('numeric_raw'+str(len(captures)),r.stdout),'stderr':save('numeric_stderr'+str(len(captures)),r.stderr)});assert r.returncode==0;return r
p=GetOnly(pins['account_tool']['path'],pins['account_tool']['sha256'],'/Users/alec/Documents/Math');start=datetime.datetime.now(datetime.timezone.utc).isoformat();numeric=mods['numeric'].observe(p);np=save('numeric_complete',jb(numeric));passes=[]
for j in range(2):
 records={};pages=[]
 for n in range(1,10001):
  raw=p.owned_page(n);x=C.strict_json(raw);pages.append({'page':n,'http_status':200,'capture':save('owned_pass'+str(j)+'_page'+str(n),raw)});assert type(x)is list and len(x)<=25
  for v in x:
   assert type(v)is dict and type(v.get('id'))is int and v['id']>0 and type(v.get('metadata'))is dict and type(v.get('files'))is list;k=str(v['id']);assert k not in records;records[k]=v
  if not x:break
 else:raise RuntimeError('No empty terminal')
 passes.append({'records':records,'pages':pages});save('owned_complete_pass'+str(j),jb(passes[-1]))
local=p.local_evidence();scientific=[]
for s in local:
 value=s['value'];manifest=None
 for key in ['manifest','manifest_path']:
  if type(value.get(key))is str:
   q=Path(value[key]);q=q if q.is_absolute()else Path('/Users/alec/Documents/Math')/q
   if q.is_file():
    b=q.read_bytes();manifest={'path':str(q),'sha256':sha(b),'value':C.strict_json(b)};break
 scientific.append({'state':s,'scientific_manifest':manifest})
lp=save('local_complete_scientific',jb(scientific));equal=C.typed_equal(passes[0]['records'],passes[1]['records']);out={'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'numeric':np,'numeric_raw':captures,'rows':len(numeric['values']),'columns':43,'owned_counts':[len(x['records'])for x in passes],'owned_two_passes_full_typed_equal':equal,'owned_complete':[save('owned_complete_pass'+str(j),jb(v))for j,v in enumerate(passes)],'empty_terminal_pages':[x['pages'][-1]['page']for x in passes],'local':lp,'local_count':len(scientific),'scientific_manifest_count':sum(x['scientific_manifest']is not None for x in scientific),'dated_only':True,'action_authority':False};(O/'INITIAL_READONLY_COLLECTION.json').write_bytes(jb(out));print(json.dumps(out));assert equal,'Full owned passes drift'
