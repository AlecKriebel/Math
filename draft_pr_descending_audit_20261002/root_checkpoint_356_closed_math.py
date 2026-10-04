"""Scoped main checkpoint of completed math audits; no priority/preprint promotion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr356_30001552'
PREFIX='checkpoint_356_closed_math'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
assert not (P/(PREFIX+'_receipt.json')).exists()
assert not (P/(PREFIX+'_stage.json')).exists(),'Never overwrite an existing or uncertain mutation attempt.'
c=json.loads((A/'ROOT_CLOSED_MATH_FAMILIES.json').read_bytes())
assert c['status']=='PASS_THREE_CLOSED_MATH_FAMILIES_FULL_AND_PUBLIC_VERIFIERS'
d=json.loads((A/'acceptance_criteria.json').read_bytes());assert d['mathematical_audit_percent']==100 and not d['candidate_accepted']
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 paths.add(str(p.relative_to(R)))
for name in ['.gitignore','ROOT_MATHEMATICAL_AUDIT.md','root_reproduce_independent_controls.py','ROOT_INDEPENDENT_CONTROLS_REPLAY.json','root_close_math_families.py','ROOT_MATH_FAMILY_CLOSURE_AUTHORIZATION.json','ROOT_CLOSED_MATH_FAMILIES.json','acceptance_criteria.json','README.md','RESEARCH_LOG.md']:
 add(A/name)
for folder in ['signed_graph_review/proposed_namespace/public','word_overlap_review/public','definition_counterexample_review/public']:
 for p in (A/folder).rglob('*'):
  if p.is_file():
   assert p.suffix in {'.py','.md','.json','.stdout'}
   add(p)
for name in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_364_tracker_356_intake_receipt.json',Path(__file__).name]:add(P/name)
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'explicit_owned_paths':sorted(paths),'mathematical_audit_percent':100,'workflow_percent':30,'scope':'Completed PR356 mathematical audit and public evidence only. Priority/preprint pending; no private source/capture publication, excluded-status processing or active priority namespace writes.'},indent=2)+'\n')
git=lambda *a:subprocess.check_output(['git',*a],cwd=R)
def window():assert not json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
 out={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1)
   if name.decode() not in paths:out.setdefault(name,[]).append(meta)
 return out
before=foreign();parent=git('rev-parse','HEAD').decode().strip()
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Verify alternating antimorphic conjecture with three independent mathematical audits','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 window();started=utc();r=subprocess.run(args,cwd=R,capture_output=True)
 for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  target=P/(PREFIX+'_'+label+'.'+name);assert not target.exists();target.write_bytes(b)
 target=P/(PREFIX+'_'+label+'.json');assert not target.exists()
 target.write_text(json.dumps({'argv':args,'cwd':str(R),'started_utc':started,'finished_utc':utc(),'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
 assert r.returncode==0,(label,r.stderr.decode(errors='replace'))
 assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
receipt={'utc':utc(),'status':'PASS_COMPLETED_PR356_MATH_CHECKPOINT_PUSHED_FULL_READBACK','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,'foreign_staged_entries_preserved':True,'mathematical_audit_percent':100,'workflow_percent':30,'priority_preprint_pending':True,'promoted':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
