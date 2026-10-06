"""Checkpoint PR344 exact-source mathematical audit, preserving all foreign index/worktree state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr344_30005649'
PREFIX='checkpoint_344_intake'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
assert load(A/'ROOT_SUBMITTED_REPRODUCTION.json')['status']=='PASS_COMPLETE_SUBMITTED_MANIFESTS_AND_TWO_WHOLE_NATIVE_REPLAYS'
assert load(A/'ROOT_ODD_DEGREE_VERIFICATION.json')['status']=='PASS_ACTUAL_F343_DEGREE_THREE_SCALAR_TWIST_AND_NONPRIME_BASIS_CONTROLS'
assert load(A/'ROOT_FROZEN_GIT_VERIFICATION.json')['all_16_blob_bytes_modes_exact']
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink()
 assert p.resolve().is_relative_to(P)
 assert not any(part.startswith('private_') or part.endswith('_private') or part=='__pycache__' for part in p.relative_to(R).parts)
 paths.add(str(p.relative_to(R)))
for n in ['README.md','RESEARCH_LOG.md','inventory.json','SHARED_GIT_WINDOW_STATUS.json','STATUS_FILTER_LEDGER.json','root_filter_next_claimed.py','checkpoint_356_final_receipt.json','STATUS_FILTER_ID_REPAIR_20261004.json',Path(__file__).name]:add(P/n)
for p in A.iterdir():
 if p.is_file() and (p.suffix in ('.py','.md','.json','.txt') or p.name=='.gitignore'):add(p)
for p in (A/'snapshot').rglob('*'):
 if p.is_file():add(p)
original=load(A/'snapshot_manifest.json')
for e in original['files']:
 b=(A/'snapshot'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'workflow_percent':16,'math_percent':65,'scope':'Only owned PR344 source-first intake, immutable original snapshot, root mathematical/classification checks and actual whole submitted/odd-degree replays, plus claimed-only status-filter ID repair and prior completed PR356 receipt. Three still-active reviewer namespaces, raw copyrighted/private captures, unrelated work and native queue state excluded.'},indent=2)+'\n')
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
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint source-matched quasi-supersingular counterexample audit and native reproductions','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 window();started=utc()
 (P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 z=subprocess.run(args,cwd=R,capture_output=True)
 for k,b in [('stdout',z.stdout),('stderr',z.stderr)]:(P/(PREFIX+'_'+label+'.'+k)).write_bytes(b)
 (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':z.returncode,'stdout_sha256':sha(z.stdout),'stderr_sha256':sha(z.stderr)},indent=2)+'\n')
 assert z.returncode==0,(label,z.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
r={'utc':utc(),'status':'PASS_PR344_ROOT_SOURCE_PROOF_NATIVE_REPRODUCTION_CHECKPOINT_PUSHED','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,'foreign_index_and_dirty_file_bytes_modes_preserved':True,'workflow_percent':16,'math_percent':65,'independent_families_still_active':3,'pr344_merged_or_published':False,'persistent_goal_complete':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
