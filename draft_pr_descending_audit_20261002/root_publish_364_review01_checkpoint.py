"""Publish only owned public first-review findings and the narrowed goal scope.

The second review remains in progress and is excluded. No excluded-status PR
is inspected or changed. Preserve every unrelated staged entry exactly.
"""
from pathlib import Path
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr364_30004048';B=A/'preprint_review_01'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((B/'MANIFEST.json').read_bytes())=='739cbb15edce4e78bd6cc5d23899a374926614b22b9dcdb493187890bd59d511'
assert sha((B/'FINAL_SEAL.json').read_bytes())=='fb2c374ddcf1d40f8c24949c8d89ee1b57f293c4d1bb4054b646ac9cdcf27677'
assert json.loads((A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json').read_bytes())['status']=='PASS_ROOT_COMPLETE_REVIEW01_READ_AND_CLOSURE'
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 rel=p.relative_to(P)
 assert not any(x=='private' or x.startswith('private_') or x in {'tmp','__pycache__','root_replay_private','root_primary_private'} for x in rel.parts[:-1])
 assert p.suffix not in {'.pdf','.zip','.png'}
 paths.add(str(p.relative_to(R)))
m=json.loads((B/'MANIFEST.json').read_bytes())
for n,e in m['files'].items():
 if Path(n).parts[0]=='private':continue
 b=(B/n).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(B/n)
add(B/'MANIFEST.json');add(B/'FINAL_SEAL.json')
for n in ['CURRENT_PREPRINT_STATUS.json','GIT_PREPARATION_PUBLICATION_RECEIPT.json','ROOT_PREPRINT_REVIEW01_VERIFICATION.json','ROOT_PREPRINT_REVIEW01_MANIFEST_SEMANTICS.json','ROOT_PREPRINT_REVIEW01_CONTROL_REPRODUCTION.json','root_reproduce_preprint_review01_control.py','root_refresh_claimed_queue.py','root_integrate_claimed.py','acceptance_criteria.json','README.md','RESEARCH_LOG.md']:add(A/n)
for n in ['README.md','run_zenodo_step.py','verify_public_record.py','append_tracker.py']:add(A/'publication'/n)
for n in ['CURRENT_SCOPE.json','inventory.json','RESEARCH_LOG.md','checkpoint_364_preprint_publication_receipt.json',Path(__file__).name]:add(P/n)
allow=P/'checkpoint_364_review01_allowlist.json';paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_owned_paths':sorted(paths),'math_percent':100,'preprint_percent':90,'acceptance_publication_workflow_percent':70,'second_fresh_review_pending':True,'scope':'Only eligible claimed_solved PR364 and current goal bookkeeping; private evidence and active second review excluded.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert subprocess.run(['git','merge-base','--is-ancestor','f91b355fcee5465d8a942d142e1bad4eabdbb1db','HEAD'],cwd=R).returncode==0
def foreign():
 out={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1)
   if name.decode() not in paths:out.setdefault(name,[]).append(meta)
 return out
before=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint first fresh biconstrained preprint review and claimed-solved-only scope','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(args,cwd=R,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (P/('checkpoint_364_review01_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_364_review01_'+label+'.stderr')).write_bytes(r.stderr)
 (P/('checkpoint_364_review01_'+label+'.json')).write_text(json.dumps({'argv':args,'cwd':str(R),'started_utc':start,'finished_utc':end,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
 assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PUBLISHED_FIRST_FRESH_PR364_REVIEW_AND_NEW_SCOPE','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True,'mathematical_resolution_percent':100,'preprint_workflow_percent':90,'acceptance_publication_workflow_percent':70,'second_review_pending':True,'merge_zenodo_tracker_pending':True,'eligible_scope':'submitted claimed_solved exactly; skip every other status and PR8'}
(P/'checkpoint_364_review01_publication_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
