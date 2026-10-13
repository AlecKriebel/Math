"""Release PR356 publication findings, preserving all foreign index/worktree state."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr356_30001552'
PREFIX='checkpoint_356_final'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
status=load(A/'CURRENT_PUBLICATION_STATUS.json')
assert status['status']=='MERGED_PUBLISHED_AND_TRACKER_VERIFIED' and status['workflow_completion_percent']==100
assert load(A/'ROOT_POST_MERGE_VERIFICATION.json')['status']=='PASS_COMPLETE_PR356_POST_MERGE'
assert load(A/'publication/TRACKER_COMPLETE.json')['doi']==status['doi']
assert load(A/'publication/PUBLIC_RECORD_VERIFICATION.json')['doi']==status['doi']
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink()
 assert p.resolve().is_relative_to(P) or p.resolve().is_relative_to(R/'problems/30001552_antimorphic_periods/preprint')
 assert not any(part.startswith('private_') or part.endswith('_private') or part=='__pycache__' for part in p.relative_to(R).parts)
 paths.add(str(p.relative_to(R)))
for n in ['README.md','RESEARCH_LOG.md','inventory.json','SHARED_GIT_WINDOW_STATUS.json','STATUS_FILTER_LEDGER.json','root_filter_next_claimed.py','checkpoint_356_review02_receipt.json',Path(__file__).name]:add(P/n)
for p in A.iterdir():
 if p.is_file() and (p.suffix in ('.py','.md','.json','.txt') or p.name=='.gitignore'):add(p)
for p in (A/'repaired_snapshot').rglob('*'):
 if p.is_file():add(p)
for p in (A/'publication').iterdir():
 if p.is_file() and p.suffix in ('.py','.md','.json','.stdout','.stderr'):add(p)
for n in ['PUBLICATION_RESULT.json','PUBLICATION.md']:add(R/'problems/30001552_antimorphic_periods/preprint'/n)
for e in load(A/'PUBLISHING_CLEARANCE.json')['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert (R/'problems/30001552_antimorphic_periods/preprint'/e['path']).read_bytes()==b
original=load(A/'snapshot_manifest.json')
for e in original['files']:
 if e['path'].endswith('/QUEUE.md'):continue
 b=(R/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'workflow_percent':100,'scope':'Only PR356 claimed-solved exact-source acceptance, unchanged reviewed submission, actual production publication and verified one-row registration. Closed review namespaces unchanged; raw private captures and generated references excluded.'},indent=2)+'\n')
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
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish verified alternating antimorphic theorem with exact Zenodo DOI and tracker receipts','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 window();started=utc()
 (P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 z=subprocess.run(args,cwd=R,capture_output=True)
 for k,b in [('stdout',z.stdout),('stderr',z.stderr)]:(P/(PREFIX+'_'+label+'.'+k)).write_bytes(b)
 (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':z.returncode,'stdout_sha256':sha(z.stdout),'stderr_sha256':sha(z.stderr)},indent=2)+'\n')
 assert z.returncode==0,(label,z.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
r={'utc':utc(),'status':'PASS_PR356_ACCEPTANCE_PUBLICATION_AND_TRACKER_CHECKPOINT_PUSHED','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,'foreign_index_and_dirty_file_bytes_modes_preserved':True,'workflow_percent':100,'doi':status['doi'],'actual_merge':status['actual_merge'],'tracker_range':status['tracker_updated_range'],'persistent_goal_complete':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
