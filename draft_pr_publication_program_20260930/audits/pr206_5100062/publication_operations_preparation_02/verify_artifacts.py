"""Read-only local verification of the sealed source-only family02 package."""
from pathlib import Path, PurePosixPath
import ast, hashlib, json, stat
D=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 raw=p.read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def load(p):return json.loads(p.read_bytes(),parse_constant=lambda value:(_ for _ in ()).throw(RuntimeError('Nonfinite JSON')))
def main():
 manifest=load(D/'SAFE_MANIFEST.json');seal=load(D/'SEAL.json')
 need(pin(D/'SAFE_MANIFEST.json')==seal['manifest_pin'],'Manifest pin differs')
 names=set()
 for e in manifest['files']:
  rel=e['path'];q=PurePosixPath(rel)
  need(type(rel) is str and not q.is_absolute() and '..' not in q.parts and rel not in names,'Unsafe/repeated payload')
  p=D/rel;need(p.resolve()==p and p.is_file() and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444,'Nonregular/nonreadonly payload')
  need(pin(p)=={k:e[k] for k in ('bytes','sha256')},'Changed payload: '+rel);names.add(rel)
 actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}
 need(actual==names|{'SAFE_MANIFEST.json','SEAL.json'},'Extra or omitted file')
 need(not any(p.is_symlink() for p in D.rglob('*')),'Symlinked payload tree')
 need(not any(p.suffix in ('.pyc','.pyo') or '__pycache__' in p.parts for p in D.rglob('*')),'Bytecode found')
 need(all(stat.S_IMODE((D/n).stat().st_mode)==0o444 for n in ('SAFE_MANIFEST.json','SEAL.json')),'Unsealed manifest/seal')
 sources=load(D/'FINAL_SOURCE_PINS.json');need(sources==seal['source_pins'],'Source map/seal differs')
 for n,w in sources.items():
  need(pin(D/n)==w,'Source changed')
  need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse((D/n).read_bytes()))),'Assert guard in five-source family')
 binding=load(D/'FAMILY02_FINAL_05_BINDINGS.json')
 need(pin(D/'FAMILY02_FINAL_05_BINDINGS.json')==seal['final_binding_pin'] and binding['status']=='PASS' and binding['active_checks_each']==660,'Final outcome differs')
 results=[]
 for e in binding['executions']:
  for name in sources:
   for key in ('code_before','code_after'):
    need({k:e[key][name][k] for k in ('bytes','sha256')}==sources[name] and e[key][name]['mode']=='0o444','Final execution source differs')
  label='OPTIMIZED' if '-O' in e['argv'] else 'NORMAL'
  for suffix,key in (('stdout','stdout'),('stderr','stderr'),('json','result')):
   need(pin(D/('FAMILY02_FINAL_05_'+label+'.'+suffix))==e[key],'Raw/result pin differs')
  need(e['exit']==0 and not (D/('FAMILY02_FINAL_05_'+label+'.stderr')).read_bytes(),'Final failure/stderr')
  result=load(D/('FAMILY02_FINAL_05_'+label+'.json'))
  need(load(D/('FAMILY02_FINAL_05_'+label+'.stdout'))==result and result['active_checks']==660 and result['real_process_or_network_calls']==0,'Final parsed outcome differs')
  result.pop('optimization_flag');results.append(result)
 need(len(results)==2 and results[0]==results[1],'Normal/-O comparison differs')
 need(len(names)==seal['payload_file_count'],'Payload count differs')
 print(json.dumps(dict(status='PASS',payload_files=len(names),final_active_checks_each=660,actual_service_calls=0,scope='Read-only artifact integrity; no Root authority or operations'),sort_keys=True))
if __name__=='__main__':main()
