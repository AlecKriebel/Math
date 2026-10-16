"""Root buffer-authenticated PR205 native lifecycle; ref movement remains external."""
import sys
if not(sys.flags.ignore_environment==1 and sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Python -E -S -B -P without -O required before dependency imports')
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,stat,types
D=Path(__file__).resolve().parent;A=D.parent;AUDITS=A.parent;P=AUDITS.parent;ROOT=P.parent
OWN='publication_lifecycle_preparation_01'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def checked(path,wanted,readonly=True):
 need(path.is_absolute() and path.is_relative_to(ROOT),'Outside checkout')
 for q in (path,*path.parents):
  if q==ROOT.parent:break
  need(not q.is_symlink(),'Symlink input '+str(q))
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 try:
  s=os.fstat(fd);need(stat.S_ISREG(s.st_mode) and s.st_size<=2000000 and (not readonly or stat.S_IMODE(s.st_mode)==0o444),'Regular bounded input')
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(2000001)
 finally:os.close(fd)
 need(pin(raw)==wanted,'Exact source/input '+str(path));return raw
def changed_buffer(path,raw):
 if path==AUDITS/'pr179_10800007/prepare_final_scoped_merge.py':
  edits=[(b"if TREE_CACHE_PATH.exists():\n for key,rows in json.loads(TREE_CACHE_PATH.read_text())['trees'].items():\n  verify_tree_object(key,rows);native_tree_cache[key]={n:tuple(x) for n,x in rows.items()}\n",b'# Root: legacy disk-cache read disabled in this execution buffer.\n'),(b'atexit.register(persist_authenticated_tree_cache)\n',b'# Root: legacy exit writer registration disabled in this execution buffer.\n')]
  for old,new in edits:need(raw.count(old)==1,'Exact accepted cache edit');raw=raw.replace(old,new,1)
 return raw
class BufferLoader:
 def __init__(self,path,raw):self.path,self.raw=path,raw
 def create_module(self,spec):return None
 def exec_module(self,module):exec(compile(self.raw,str(self.path),'exec'),module.__dict__)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--adoption',required=True);ap.add_argument('--adoption-bytes',required=True,type=int);ap.add_argument('--adoption-sha256',required=True);ap.add_argument('phase',choices=['ready','merge','factual','completion']);ap.add_argument('action',choices=['preflight','bind','prepare','verify','accept','sync','pointer']);ap.add_argument('generation');ap.add_argument('--ack-path');ap.add_argument('--ack-bytes',type=int);ap.add_argument('--ack-sha256');args=ap.parse_args()
 need(Path(args.adoption).name==args.adoption and args.adoption not in ('.','..'),'Fixed adoption basename')
 wanted=dict(bytes=args.adoption_bytes,sha256=args.adoption_sha256);adopt=json.loads(checked(A/args.adoption,wanted));checked(Path(__file__),adopt['runner_pin'])
 need(adopt.get('schema')=='pr205-root-lifecycle-preparation-adoption-v1' and adopt.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adopt.get('accepted_preparation_only') is True and adopt.get('PR')==205 and adopt.get('original_head')=='e8d7e925d19698edcb75822e40ca5ac820eb4388','Exact Root adoption')
 expected_sources={OWN+'/'+n for n in ['support205.py','ready205.py','lifecycle205.py','make_native205.py']};need(set(adopt['sources'])==expected_sources,'Exact four proposal sources')
 buffers={}
 for name,x in adopt['sources'].items():buffers[A/name]=checked(A/name,x)
 backend={}
 for name,x in adopt['loader_sources'].items():
  q=ROOT/name;raw=checked(q,x['original'],x['readonly']);body=changed_buffer(q,raw);need(pin(body)==x['execution'],'Accepted backend execution buffer');backend[q]=body
 aliases=['Root_support205','Root_ready205','Root_native205','Root_lifecycle205'];present={n:n in sys.modules for n in aliases};prior={n:sys.modules.get(n) for n in aliases};original_spec=importlib.util.spec_from_file_location;cache=None;mods=[];original_api=None
 def direct(name,path):
  v=types.ModuleType(name);v.__file__=str(path);v.__package__='';sys.modules[name]=v;exec(compile(buffers[path],str(path),'exec'),v.__dict__);return v
 def guarded_spec(name,path,*aa,**kw):
  q=Path(path);need(q.is_absolute() and q in backend and not aa and not kw,'Unapproved backend source '+str(q));spec=original_spec(name,q);need(spec is not None,'Backend spec');spec.loader=BufferLoader(q,backend[q]);return spec
 def native(name,path):
  sp=guarded_spec(name,path);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);return v
 try:
  S=direct(aliases[0],A/OWN/'support205.py');S.configure_authority(args.adoption,wanted)
  R=direct(aliases[1],A/OWN/'ready205.py');N=direct(aliases[2],A/OWN/'make_native205.py');L=direct(aliases[3],A/OWN/'lifecycle205.py')
  R.configure(S);N.configure(S);L.configure(S,R,N);gpin={k:adopt['expected_publication_gate'][k] for k in ('bytes','sha256')};S.gate(gpin);S.baseline_intake();S.originals();S.queue_rows()
  ack=None
  if args.phase!='ready':
   need(args.ack_path is not None and args.ack_bytes is not None and args.ack_sha256 is not None,'Explicit actual metadata ACK')
   ack=dict(path=args.ack_path,bytes=args.ack_bytes,sha256=args.ack_sha256)
  else:need(args.ack_path is None and args.ack_bytes is None and args.ack_sha256 is None,'No metadata ACK at ready90')
  if args.action=='preflight':
   if args.phase!='ready':L.inputs(args.phase,ack)
   print(json.dumps(dict(PR=205,phase=args.phase,preflight=True,authenticated_sources=len(buffers)+len(backend),backend_import_or_API_or_cache_install_or_phase=False),sort_keys=True));return
  if args.action=='bind':
   result=R.bind(args.generation,gpin) if args.phase=='ready' else L.bind(args.phase,args.generation,ack)
   print(json.dumps(result,sort_keys=True));return
  importlib.util.spec_from_file_location=guarded_spec
  c=native('Root_c191_205',AUDITS/'pr191_5000005/lifecycle_common.py');h=native('Root_h190_205',AUDITS/'pr190_5000007/prepare_final_scoped_merge.py');adapter=native('Root_tree_adapter205',AUDITS/'pr204_5100012/immutable_tree_transport_01/tree_transport.py')
  mods=[h,h.m,h.m.m,h.m.m.h,h.m.m.h.m,h.m.m.h.m.m];original_api=h.api
  need(len({id(m) for m in mods})==6 and all(m.api is original_api for m in mods),'Six API aliases equal')
  need(h.m.native_tree_cache is h.lookup.__globals__['TREE_CACHE'] and not h.m.native_tree_cache,'No inherited cache')
  S.configure_backend(c,h)
  original_init=adapter.TreeCache.__init__
  def capture_init(instance,*aa,**kw):
   nonlocal cache
   cache=instance;instance.fd=None
   return original_init(instance,*aa,**kw)
  adapter.TreeCache.__init__=capture_init
  try:cache,_restore=adapter.install_loaded(c,h)
  finally:adapter.TreeCache.__init__=original_init
  if args.action in ('prepare','verify','accept'):result=R.run(args.action,args.generation) if args.phase=='ready' else L.run(args.phase,args.action,args.generation)
  elif args.action=='sync':result=R.sync(args.generation) if args.phase=='ready' else L.sync(args.phase,args.generation)
  else:result=R.pointer(args.generation) if args.phase=='ready' else L.pointer(args.phase,args.generation)
  print(json.dumps(result,sort_keys=True))
 finally:
  errors=[]
  if mods:
   for m in mods:
    try:
     if m.api is not cache and m.api is not original_api:errors.append('API alias changed before restoration')
     m.api=original_api
    except BaseException as exc:errors.append(type(exc).__name__+':'+str(exc))
  if cache is not None:
   try:cache.close()
   except BaseException as exc:errors.append(type(exc).__name__+':'+str(exc))
  importlib.util.spec_from_file_location=original_spec
  for n in aliases:
   try:
    if present[n]:sys.modules[n]=prior[n]
    else:sys.modules.pop(n,None)
   except BaseException as exc:errors.append(type(exc).__name__+':'+str(exc))
  if cache is not None:print(json.dumps(dict(transport_stats=getattr(cache,'stats',{}),all_six_API_restore_attempted=True,cleanup_errors=errors),sort_keys=True))
  if errors:raise RuntimeError('Lifecycle cleanup failed: '+repr(errors))
if __name__=='__main__':main()
