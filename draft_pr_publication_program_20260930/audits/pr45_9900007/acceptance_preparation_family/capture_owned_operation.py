"""Capture only own handwritten source authoring, controls or closure; production remains text."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys
H=Path(__file__).resolve().parent
ALLOWED={'author_sources.py','bind_actual_whole_review.py','independent_controls.py','close_source.py','repair_sources.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(o):return (json.dumps(o,sort_keys=True,indent=2)+'\n').encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('capture');p.add_argument('script');a=p.parse_args()
 if not __debug__ or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('Optimization prohibited')
 if a.script not in ALLOWED or not a.capture or '/' in a.capture or a.capture in {'.','..'}:raise ValueError('Own allowlisted source only')
 s=H/a.script;source=s.read_bytes();operator=Path(__file__).read_bytes();outdir=H/a.capture;outdir.mkdir(mode=0o755)
 pre={'schema':'pr45-source-operation-prelaunch/v1','operator_pid':os.getpid(),'script':str(s),'source_sha256':sha(source),'operator_sha256':sha(operator),'cwd':str(H),'created_utc':now(),'argv':[sys.executable,'-B',str(s)],'stdin_supplied':False}
 put(outdir/'PRELAUNCH_SOURCE.py',source);put(outdir/'PRELAUNCH_OPERATOR.py',operator);put(outdir/'PRELAUNCH.json',enc(pre))
 start=now();child=subprocess.Popen(pre['argv'],cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();end=now()
 rec={'schema':'pr45-source-operation-actual-capture/v1','prelaunch':pre,'operator_pid':os.getpid(),'pid':child.pid,'actual_execution':True,'completed':True,'exit_code':child.returncode,'started_utc':start,'finished_utc':end,'source_unchanged':s.read_bytes()==source,'operator_unchanged':Path(__file__).read_bytes()==operator}
 for channel,b in [('stdout',out),('stderr',err)]:
  put(outdir/(channel+'.bin'),b);rec[channel]={'path':channel+'.bin','bytes':len(b),'sha256':sha(b)}
 rec['status']='PASS' if child.returncode==0 and rec['source_unchanged'] and rec['operator_unchanged'] else 'FAIL';put(outdir/'CAPTURE.json',enc(rec))
 if a.script=='close_source.py' and rec['status']=='PASS':
  import stat
  members=[]
  for p in sorted(H.rglob('*')):
   if p.is_symlink() or not (p.is_file() or p.is_dir()):raise ValueError('Unsafe closed SOURCE member')
   if p.is_file():
    if p.name=='PREPARATION_MANIFEST.json':raise ValueError('Existing closure prohibited')
    p.chmod(0o444);b=p.read_bytes();members.append({'path':p.relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b)})
  mf={'schema':'pr45-acceptance-source-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':now(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(members),'files':members,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False}
  put(H/'PREPARATION_MANIFEST.json',enc(mf));(H/'PREPARATION_MANIFEST.json').chmod(0o444)
  for p in H.rglob('*'):
   if p.is_file() and stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('Literal full0444 SOURCE closure')
  print(json.dumps({'status':'CLOSED_SOURCE_ONLY','manifest_sha256':sha((H/'PREPARATION_MANIFEST.json').read_bytes()),'members_excluding_self':len(members),'closure_child_pid':child.pid,'outer_operator_pid':os.getpid(),'actual_capture':a.capture,'full_mode':'0444','production_executed':False,'future_ROOT_acceptance_approved':False},sort_keys=True))
 else:print(json.dumps({'capture':a.capture,'operator_pid':os.getpid(),'child_pid':child.pid,'status':rec['status'],'exit_code':child.returncode,'stdout':out.decode(errors='replace'),'stderr':err.decode(errors='replace')},sort_keys=True))
 return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
