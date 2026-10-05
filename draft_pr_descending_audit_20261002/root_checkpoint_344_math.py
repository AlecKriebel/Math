"""Scoped mathematical checkpoint; preserve all foreign index/body/mode state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr344_30005649'
PREFIX='checkpoint_344_math'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
accepted=load(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json')
assert accepted['status']=='MATHEMATICS_ACCEPTED_THREE_INDEPENDENT_FAMILIES_AND_ROOT' and accepted['mathematical_completion_estimate_percent']==100
for family,record in accepted['families'].items():
 for relative,pin in record['whole_current_namespace'].items():
  f=A/family/relative;b=f.read_bytes();assert sha(b)==pin['sha256'] and len(b)==pin['bytes'] and f.stat().st_mode&0o7777==pin['mode']
window()
shared_path=P/'SHARED_GIT_WINDOW_STATUS.json';shared=load(shared_path)
shared.update({'utc':utc(),'descending_git_checkpoint_preparing':True,'descending_git_checkpoint_scope':'PR344 completed three-family mathematical validation and portable controls only; no merge/publication.'})
shared_path.write_text(json.dumps(shared,indent=2)+'\n')
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 assert not any(part.startswith('private_') or part.endswith('_private') or part=='__pycache__' for part in p.relative_to(R).parts)
 paths.add(str(p.relative_to(R)))
for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','root_pause_pr50_20261004.py','root_resume_pr50_20261004.py','checkpoint_344_intake_receipt.json',Path(__file__).name]:add(P/n)
for p in A.iterdir():
 if p.is_file() and (p.suffix in ('.py','.md','.json','.txt') or p.name=='.gitignore'):add(p)
for n in ['semilinear_proof.md','audit_report.md','verify_semilinear.py']:add(A/'semilinear_modules'/n)
for n in ['REPORT.md','check_realization.py']:add(A/'honda_lifting'/n)
for p in (A/'intrinsic_invariants'/'public').iterdir():
 if p.is_file():add(p)
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'workflow_percent':30,'math_percent':100,'scope':'Only owned PR344 completed root/family mathematical proofs and portable algebra controls, root precise acceptance/closure metadata and scoped scripts, plus shared PR50 pause/resume root logs and previous intake checkpoint receipt. Raw copyrighted sources, private native reading streams, reviewer private namespaces and unrelated/native queue state excluded. No PR344 merge or publication.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
assert git('branch','--show-current')==b'main\n' and not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
 entries={};bodies={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1)
   if name.decode() not in paths:entries.setdefault(name,[]).append(meta)
 for name in git('diff','--name-only','-z').split(b'\0'):
  if name and name.decode() not in paths:
   f=R/name.decode();bodies[name]={'exists':f.exists(),'bytes':f.read_bytes() if f.is_file() else None,'mode':f.stat().st_mode&0o7777 if f.exists() else None}
 return entries,bodies
window();before=foreign();parent=git('rev-parse','HEAD').decode().strip()
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Validate quasi-supersingular counterexample through three independent mathematical audits','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 window();started=utc()
 (P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 z=subprocess.run(args,cwd=R,capture_output=True)
 for k,b in [('stdout',z.stdout),('stderr',z.stderr)]:(P/(PREFIX+'_'+label+'.'+k)).write_bytes(b)
 (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':z.returncode,'stdout_sha256':sha(z.stdout),'stderr_sha256':sha(z.stderr)},indent=2)+'\n')
 assert z.returncode==0,(label,z.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
r={'utc':utc(),'status':'PASS_PR344_COMPLETE_MATHEMATICAL_AUDIT_CHECKPOINT_PUSHED','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,'foreign_index_and_dirty_file_bytes_modes_preserved':True,'workflow_percent':30,'math_percent':100,'independent_families_closed':3,'priority_complete':False,'pr344_merged_or_published':False,'persistent_goal_complete':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
shared=load(shared_path)
shared.update({'utc':utc(),'descending_git_checkpoint_preparing':False,'last_owned_checkpoint':commit,'last_owned_checkpoint_pushed':True})
shared_path.write_text(json.dumps(shared,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n### '+utc()+' — PR344 mathematical checkpoint pushed\n\nCommit '+commit+' pushed to main after exact scoped Git/disk and remote verification; all foreign index and dirty tracked bodies/modes preserved. Three independent mathematical families closed; mathematical completion100%, publication workflow30%. Priority audit next. No PR344 merge or publication.\n')
