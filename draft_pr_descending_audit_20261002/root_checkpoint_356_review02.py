"""Checkpoint two sequential clean fresh preprint reviews and exact-live preparation."""
from pathlib import Path
import datetime,hashlib,json,subprocess,os
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr356_30001552'
PREFIX='checkpoint_356_review02'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def window():assert not json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
assert json.loads((A/'PUBLISHING_CLEARANCE.json').read_bytes())['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert json.loads((P/'ROOT_COMPLETED_NATIVE_CAPTURE_COMPRESSION_20261004T0228.json').read_bytes())['status']=='COMPLETE_ALL_ARCHIVES_VERIFIED'
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 paths.add(str(p.relative_to(R)))
for name in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_356_review01_receipt.json',Path(__file__).name]:add(P/name)
for name in ['README.md','RESEARCH_LOG.md','acceptance_criteria.json','root_verify_preprint_review02.py','ROOT_PREPRINT02_SOURCE_GATE.json','ROOT_PREPRINT02_PRECLOSURE_REPLAY.json','ROOT_PREPRINT02_CLOSURE_AUTHORIZATION.json','ROOT_PREPRINT_REVIEW02_VERIFICATION.json','root_submission_gate.py','root_clear_submission.py','PUBLISHING_CLEARANCE.json','CURRENT_PREPRINT_STATUS.json','root_refresh_claimed_queue.py','root_verify_exact_live.py','root_integrate_claimed.py','root_verify_post_merge.py','accepted_pr_body.txt','merge_body.txt']:add(A/name)
n=A/'preprint_review_02';assert sha((n/'CLOSURE_SEAL.json').read_bytes())=='32195f52ba68d9a64aa668cedd426e31c7ab5930c4022d4ef161334fc3d6bfad'
for name in json.loads((n/'PUBLIC_MANIFEST.json').read_bytes())['files']:add(n/name)
add(n/'PUBLIC_MANIFEST.json');add(n/'CLOSURE_SEAL.json')
assert json.loads((A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').read_bytes())['closed_namespace_unchanged']
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'workflow_percent':75,
 'scope':'Sealed curated second sequential fresh preprint review and root whole-stream replay/closure checks. Unchanged submission cleared after both reviews; exact-live integration preparation. No raw private data, merge, publication or tracker action.'},indent=2)+'\n')
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
before=foreign();parent=git('rev-parse','HEAD').decode().strip();assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),
 ('commit',['git','commit','--only','-m','Clear antimorphic preprint after two fresh reviews and prepare exact-source acceptance','--',*sorted(paths)]),
 ('push',['git','push','origin','main'])]:
 window();started=utc();(P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 r=subprocess.run(args,cwd=R,capture_output=True)
 for kind,b in [('stdout',r.stdout),('stderr',r.stderr)]:(P/(PREFIX+'_'+label+'.'+kind)).write_bytes(b)
 (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
 assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
r={'utc':utc(),'status':'PASS_SECOND_FRESH_PREPRINT_REVIEW_AND_CLEARANCE_CHECKPOINT_PUSHED','commit':commit,'parent':parent,
 'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,
 'foreign_index_and_dirty_file_bytes_modes_preserved':True,'workflow_percent':75,'promoted':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
