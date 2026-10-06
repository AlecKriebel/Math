from pathlib import Path
import subprocess,json,datetime,hashlib,os
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032"); C=A.parents[2]; D=A/'remote_main_advance_reconciliation_20261006';D.mkdir(exist_ok=False)
old='735a11defdf906d1552912815810ff72779874a7'; records=[]
def run(args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); p=subprocess.Popen(['git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);o,e=p.communicate()
 i=len(records);(D/(str(i)+'.stdout.bin')).write_bytes(o);(D/(str(i)+'.stderr.bin')).write_bytes(e)
 records.append({'argv':['git',*args],'PID':p.pid,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(o),'stderr_bytes':len(e),'stdout_sha256':hashlib.sha256(o).hexdigest(),'stderr_sha256':hashlib.sha256(e).hexdigest()})
 (D/'PROCESS_JOURNAL.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode:raise RuntimeError(e.decode())
 return o
new=run(['rev-parse','refs/remotes/pr110-audit-main']).decode().strip();run(['merge-base','--is-ancestor',old,new])
rows=run(['diff','--name-only','-z',old,new]).split(b'\0'); paths={x.decode() for x in rows if x}
s=set(json.loads((A/'SOURCE_MATH_CHECKPOINT_SELECTION_20261006.json').read_text())['paths'])
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'old':old,'new':new,'fast_forward_possible':True,'changed_paths':sorted(paths),'selected_collision_paths':sorted(s&paths),'commits':run(['log','--format=%H %s',old+'..'+new]).decode(),'no_mutation':True}
(D/'INSPECTION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

