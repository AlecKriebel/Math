"""Root authenticated-buffer dispatcher for PR205 publication and tracking."""
import sys
if not (sys.flags.ignore_environment==1 and sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Python -E -S -B -P without -O required before dependency imports')
from pathlib import Path
import argparse,hashlib,json,os,stat,types
D=Path(__file__).resolve().parent;A=D.parent
OWN='publication_operations_preparation_01'
PINS={
'operations_common.py':(15155,'36e251c434b7666e8ed8d5b43fe03764646367ecdd77664b38948361e4963727'),
'publish_exact.py':(11236,'fb88cae7259f7d7750f3b6dc163d14e75d9d290ae9373b0d38722d683d9cdd34'),
'update_tracker.py':(10674,'2e6d261246d9efe7a52eeaf1951d2727415ca63b2ed30a254b0ca431379d8bb5'),
'offline_tests.py':(26018,'8196e730f92573f3f0a2ec879391e6ed790340f78e433561a88736334a35c472'),
'run_offline.py':(3846,'ecaba5c357b28c30dae39de1c446de2bedac25212770600e3264c1ab312cd751')}
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def checked(path,wanted):
 need(path.is_absolute() and path.is_relative_to(A),'Path outside PR205')
 for q in (path,*path.parents):
  if q==A.parent:break
  need(not q.is_symlink(),'Symlinked source/input')
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 try:
  s=os.fstat(fd);need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_size<=2000000,'Regular readonly bounded input')
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(2000001)
 finally:os.close(fd)
 need(pin(raw)==wanted,'Exact input pin: '+path.name);return raw
def load_module(name,path,raw):
 m=types.ModuleType(name);m.__file__=str(path);m.__package__=''
 sys.modules[name]=m;exec(compile(raw,str(path),'exec'),m.__dict__);return m
def main():
 need(sys.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -E -S -B -P required')
 ap=argparse.ArgumentParser();ap.add_argument('--adoption',required=True);ap.add_argument('--adoption-bytes',required=True,type=int);ap.add_argument('--adoption-sha256',required=True)
 ap.add_argument('action',choices=['preflight','stage','inspect','publish','inspect-doi','finalize','append','recover']);ap.add_argument('--confirm-id',type=int)
 args=ap.parse_args()
 rel=Path(args.adoption);need(not rel.is_absolute() and '..' not in rel.parts and rel.name==str(rel),'Fixed adoption basename')
 wanted=dict(bytes=args.adoption_bytes,sha256=args.adoption_sha256)
 adoption=json.loads(checked(A/rel,wanted))
 need(adoption.get('schema')=='pr205-root-publication-operations-adoption-v1' and adoption.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adoption.get('accepted_preparation_only') is True and adoption.get('PR')==205 and adoption.get('original_head')=='e8d7e925d19698edcb75822e40ca5ac820eb4388','Root adoption identity')
 expected={OWN+'/'+n:dict(bytes=v[0],sha256=v[1]) for n,v in PINS.items()}
 need(adoption['sources']==expected,'Exact approved five-source set')
 checked(Path(__file__),adoption['dispatcher_pin'])
 checked(A/'ROOT_PUBLICATION_GATE_01.json',adoption['approved_publication_gate_pin'])
 buffers={n:checked(A/OWN/n,expected[OWN+'/'+n]) for n in PINS}
 aliases=['operations_common','Root_pr205_publisher','Root_pr205_tracker'];prior={n:sys.modules.get(n) for n in aliases};present={n:n in sys.modules for n in aliases};oldargv=list(sys.argv)
 try:
  c=load_module(aliases[0],A/OWN/'operations_common.py',buffers['operations_common.py'])
  c.configure_authority(str(rel),wanted)
  if args.action=='preflight':
   ctx=c.load_context(A);print(json.dumps(dict(preflight=True,PR=205,context=c.context_pin(ctx),compiled_sources=['operations_common.py'],checked_sources=len(buffers),process_or_HTTP_or_Git_calls=False),sort_keys=True));return
  tracker=args.action in ('append','recover');name='update_tracker.py' if tracker else 'publish_exact.py'
  module=load_module(aliases[2] if tracker else aliases[1],A/OWN/name,buffers[name])
  sys.argv=[str(A/OWN/name),args.action,'--base',str(A),'--adoption',str(rel),'--adoption-bytes',str(args.adoption_bytes),'--adoption-sha256',args.adoption_sha256]
  if args.confirm_id is not None:
   need(not tracker and args.action in ('inspect','publish','inspect-doi'),'Known ID only for explicit Zenodo phase');sys.argv+=['--confirm-id',str(args.confirm_id)]
  module.main()
 finally:
  sys.argv=oldargv
  for n in aliases:
   if present[n]:sys.modules[n]=prior[n]
   else:sys.modules.pop(n,None)
if __name__=='__main__':main()
