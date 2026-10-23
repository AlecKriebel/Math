"""Readonly independent postappend evidence closure.
Caller must prehash THIS file and supply whole manifest SHA/nsmtime.
No root completion receipt, actor action, service call or filesystem write.
"""
import sys
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('use isolated -I -S -B optimize0')
from pathlib import Path
import argparse,ast,base64,datetime,hashlib,json,os,stat
W=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:need(False,'nonfinite JSON'))
def eq(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return set(a)==set(b)and all(eq(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
 return a==b
def utc(x):
 need(type(x)is str,'time type');t=datetime.datetime.fromisoformat(x.replace('Z','+00:00'));need(t.utcoffset()==datetime.timedelta(0),'aware UTC');return t
def meta(p):
 s=p.lstat();return {'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'inode':s.st_ino,'device':s.st_dev}
def fp(p):
 need(p.is_file()and not p.is_symlink(),'regular file');b=p.read_bytes();return {**meta(p),'bytes':len(b),'sha256':sha(b)}
def tree(root,exclude=()):
 need(root.is_dir()and not root.is_symlink(),'regular root');f={};d={'.':meta(root)}
 for q in sorted(root.rglob('*')):
  r=str(q.relative_to(root));need(not q.is_symlink(),'no symlink')
  if q.is_dir():d[r]=meta(q)
  elif r not in exclude:f[r]=fp(q)
 return {'files':f,'directories':d}
def readonly(event,args):
 if event in {'socket.connect','socket.getaddrinfo','subprocess.Popen','os.system','os.mkdir','os.remove','os.rmdir','os.rename','os.link','os.symlink','os.truncate','os.chmod','os.utime'}:raise RuntimeError('Readonly replay forbids effect '+event)
 if event=='open':
  path,mode,flags=args
  if isinstance(mode,str)and any(c in mode for c in 'wax+')or isinstance(flags,int)and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):raise RuntimeError('Readonly replay forbids file write')
def retained_native(prefix):
 n=strict((W/(prefix+'_ORIGINAL_NATIVE.json')).read_bytes())
 need(n['argv'][1:4]==['-I','-S','-B']and type(n['returncode'])is int,'original native argv/returncode')
 need(utc(n['started_at'])<=utc(n['finished_at']),'native UTC order')
 for role in ['STDOUT','STDERR']:
  b=(W/(prefix+'_'+role+'.bin')).read_bytes();need(n[role]=={'bytes':len(b),'sha256':sha(b)},'complete original native '+prefix)
 return n
def replay_probe(script,resultfile,prefix,status,count):
 # Exact recorded script prefix through its result object. Its original final
 # O_EXCL own-result writer/print is omitted, not redirected or executed.
 path=W/script;raw=path.read_bytes();t=ast.parse(raw)
 indices=[i for i,n in enumerate(t.body)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='result'for x in n.targets)]
 need(len(indices)==1,'finite probe result boundary')
 ns={'__file__':str(path),'__name__':'readonly_original_probe_prefix'}
 exec(compile(ast.Module(body=t.body[:indices[0]+1],type_ignores=[]),str(path)+'::readonly_prefix','exec',dont_inherit=True,optimize=0),ns)
 r=strict((W/resultfile).read_bytes());n=retained_native(prefix)
 need(n['returncode']==0 and n['STDERR']['bytes']==0,'selected original native complete success')
 need(eq(ns['result'],r)and eq(strict((W/(prefix+'_STDOUT.bin')).read_bytes()),r),'complete original result/prefix replay equality')
 need(r['status']==status and r['count']==count and len(r['checks'])==count and r['actual_effects']==0,'entire retained semantic proof')
def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-nsmtime',required=True,type=int);a=p.parse_args()
 manifest=W/'MANIFEST_POSTAPPEND_REVIEW.json';raw=manifest.read_bytes();need(sha(raw)==a.manifest_sha256 and manifest.stat().st_mtime_ns==a.manifest_nsmtime,'externally pinned complete manifest')
 m=strict(raw);need(m['schema']=='independent-known23592692-postappend-getonly-review-1'and m['status']=='CLEAN_DATED_CAPTURED_PROOF_NO_ACTOR_CERTIFICATION','final scoped review')
 need(tree(W,('MANIFEST_POSTAPPEND_REVIEW.json',))==m['own_namespace'],'complete owned namespace/bytes/mode/nsmtime/nlink/inode/device')
 need(meta(manifest)==m['manifest_metadata_except_mtime']|{'mtime_ns':a.manifest_nsmtime},'manifest reserved identity')
 for x in m['external_files']:
  p=Path(x['path']);need(p.is_absolute()and not any(q.is_symlink()for q in[p,*p.parents]),'absolute immutable input')
  need(fp(p)=={k:v for k,v in x.items()if k!='path'},'entire external input bytes/metadata '+str(p))
 for x in m['external_trees']:need(tree(Path(x['path']))==x['namespace'],'entire external namespace '+x['path'])
 need(m['actual_effects']==0 and m['actor_certification']is False and m['Root_receipt_builder_reviewed']is False,'scoped review only')
 # Original failed and successful probes all remain, with full native streams.
 for prefix in m['original_native_prefixes']:retained_native(prefix)
 sys.addaudithook(readonly)
 replay_probe('original_append_ack_probe01.py','ORIGINAL_APPEND_ACK_PROBE01_RESULTS.json','ORIGINAL_APPEND_ACK_PROBE01','PASS_ORIGINAL_ACK_ONLY',9)
 replay_probe('captured_full287_sheet_probe03.py','CAPTURED_FULL287_SHEET_PROBE03_RESULTS.json','CAPTURED_FULL287_SHEET_PROBE03','PASS_CAPTURED_SHEET_ONLY',17)
 replay_probe('pure_ui_holder_native_probe02.py','PURE_UI_HOLDER_NATIVE_PROBE02_RESULTS.json','PURE_UI_HOLDER_NATIVE_PROBE02','PASS_PURE_UI_HOLDER_CAPTURED_PUBLIC_ONLY',16)
 P=W.parent;D=P/'root_actual21_known23592692_actions01';RT=P/'operations19/runtime'
 for action,rc in [('stage-known',0),('publish',0),('verify-public',0),('ledger',1)]:
  ex=strict((D/(action+'.exit.json')).read_bytes());need(ex['returncode']==rc and ex['complete_native_return']is True and ex['error']is None,'actual phase exit history')
  for role in ['stdout','stderr']:
   b=(D/(action+'.'+role+'.bin')).read_bytes();need(ex[role]=={'bytes':len(b),'sha256':sha(b)},'actual action raw stream')
 need(not(D/'ledger.parsed.json').exists()and not(RT/'LEDGER_VERIFIED.json').exists(),'never fabricate fourth success or base19 certificate')
 need((D/'ledger.stderr.bin').read_bytes().endswith(b'RuntimeError: Expired/future observation\n'),'exact known final freshness failure retained')
 print(json.dumps({'status':'PASS','manifest_sha256':sha(raw),'own_files':len(m['own_namespace']['files']),'own_directories':len(m['own_namespace']['directories']),'external_files':len(m['external_files']),'external_trees':len(m['external_trees']),'independent_actual_kernel_controls':42,'semantic_falsifiers':21,'original_native_envelopes':len(m['original_native_prefixes']),'actual_effects':0,'actor_certification':False,'Root_receipt_builder_reviewed':False,'limits':'Dated separate12:40 sheet and12:44 public captures; no old facts_fresh renewal, fourth rc0 or base ledger certificate.'},sort_keys=True))
if __name__=='__main__':main()
