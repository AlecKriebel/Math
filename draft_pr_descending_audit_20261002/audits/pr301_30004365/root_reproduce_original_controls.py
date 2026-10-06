"""Reproduce both immutable original finite controls in two actual runtimes."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).parent;SRC=A/'snapshot/problems/30004365_gentle_derived_invariant';D=A/'reproduction';sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def main():
 need(not sys.flags.optimize,'unoptimized recorder');D.mkdir(exist_ok=False);summary=[]
 for runtime,label in [(Path('/opt/homebrew/bin/python3'),'native314'),(R/'.venv/bin/python','research39')]:
  need(runtime.exists(),'available original and current interpreter')
  for relative,expected in [('verify_turn1.py','verification.json'),('review/verify_independent.py','review/INDEPENDENT_CONTROLS.json')]:
   name=label+'_'+Path(relative).stem;q=D/name;q.mkdir();source=q/Path(relative).name;source.write_bytes((SRC/relative).read_bytes());source.chmod(0o644);archive=q/'source.gz';archive.write_bytes(gzip.compress(source.read_bytes(),mtime=0));argv=[str(runtime),'-E','-B',str(source)];request=dict(argv=argv,cwd=str(q),requested_UTC=utc(),recorder=pin(__file__),source=pin(source),original_source=pin(SRC/relative),interpreter_binary=pin(runtime.resolve()),interpreter_invocation=str(runtime),unoptimized=True,automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'recorder.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=q,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);start=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(start,indent=2)+'\n');out,err=proc.communicate(timeout=55);streams={}
   for n,b in [('stdout',out),('stderr',err)]:
    f=q/(n+'.gz');f.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(f),logical_bytes=len(b),logical_sha256=sha(b))
   execution=dict(**start,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=streams);(q/'execution.json').write_text(json.dumps(execution,indent=2)+'\n');need(proc.returncode==0 and not err,'actual finite controls succeeded');need(json.loads(out)==json.loads((SRC/expected).read_bytes()),'complete original expected JSON equality');summary.append(dict(label=name,execution=pin(q/'execution.json'),actual_PID=proc.pid,full_output= json.loads(out),original_expected=pin(SRC/expected),complete_JSON_equality=True,supplementary_only=True))
 result=dict(status='PASS_ROOT_REPRODUCES_ORIGINAL_FINITE_CONTROLS_BOTH_RUNTIMES',UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(__file__),reproductions=summary,all_original_sources_unchanged=True,not_full_algorithm_implementation_or_universal_proof=True,estimates_percent=dict(mathematical_review=20,priority=0,workflow=10));p=A/'ROOT_ORIGINAL_FINITE_CONTROLS_REPRODUCTION.json';p.write_text(json.dumps(result,indent=2)+'\n');p.chmod(0o444);print(json.dumps(dict(status=result['status'],actual_recorder_PID=os.getpid(),actual_control_processes=len(summary),result=pin(p)),indent=2))
if __name__=='__main__':main()
