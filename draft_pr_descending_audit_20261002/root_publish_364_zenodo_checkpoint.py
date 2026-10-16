"""Publish only owned accepted PR364 findings, exact Zenodo receipts and tracker pending state.

No excluded-status PR is inspected or changed. Preserve every unrelated
staged entry exactly. No GitHub release, journal submission, tracker mutation or other PR processing.
"""
from pathlib import Path
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr364_30004048';B=A/'preprint_review_01'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((B/'MANIFEST.json').read_bytes())=='739cbb15edce4e78bd6cc5d23899a374926614b22b9dcdb493187890bd59d511'
assert sha((B/'FINAL_SEAL.json').read_bytes())=='fb2c374ddcf1d40f8c24949c8d89ee1b57f293c4d1bb4054b646ac9cdcf27677'
assert json.loads((A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json').read_bytes())['status']=='PASS_ROOT_COMPLETE_REVIEW01_READ_AND_CLOSURE'
clear=json.loads((A/'PUBLISHING_CLEARANCE.json').read_bytes())
assert clear['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and clear['second_review_mandatory_findings']==0
publication=json.loads((A/'PUBLICATION_RESULT.json').read_bytes())
assert publication['status']=='MERGED_AND_ZENODO_PUBLISHED_TRACKER_AUTH_PENDING' and publication['doi']=='10.5281/zenodo.23127646'
assert publication['all_ten_reviewed_metadata_keys_exact'] and publication['all_two_public_file_bytes_exact'] and publication['tracker_mutation_attempted'] is False
assert json.loads((A/'ROOT_POST_MERGE_VERIFICATION.json').read_bytes())['status']=='PASS_FRESH_POST_MERGE_ALL_SOURCE_AND_SUBMISSION_BINDINGS'
window=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())
assert not window['shared_git_writes_paused'],"Respect the ascending reviewer's announced shared Git window"
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 rel=p.relative_to(P)
 assert not any(x=='private' or x.startswith('private_') or x in {'tmp','__pycache__','root_replay_private','root_primary_private'} for x in rel.parts[:-1])
 assert p.suffix not in {'.pdf','.zip','.png'} or p.parent==A/'preprint' and p.name in {'biconstrained_asymmetry.pdf','biconstrained-asymmetry-verification.zip'}
 paths.add(str(p.relative_to(R)))
m=json.loads((B/'MANIFEST.json').read_bytes())
for n,e in m['files'].items():
 if Path(n).parts[0]=='private':continue
 b=(B/n).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(B/n)
add(B/'MANIFEST.json');add(B/'FINAL_SEAL.json')

B2=A/'preprint_review_02';root2=json.loads((A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').read_bytes())
assert root2['mandatory_findings']==0 and root2['closed_namespace_unchanged'] and root2['whole_verifier_output_compared'] and root2['review_seal_sha256']==sha((B2/'FINAL_SEAL.json').read_bytes())
m2=json.loads((B2/'MANIFEST.json').read_bytes())
for n,e in m2['files'].items():
 if Path(n).parts[0]=='private':continue
 b=(B2/n).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(B2/n)
add(B2/'MANIFEST.json');add(B2/'FINAL_SEAL.json')
for p in A.iterdir():
 if p.is_file() and (p.suffix in {'.py','.md','.json','.txt'} or p.name=='.gitignore'):add(p)
for e in clear['sealed_submission_files']:
 p=A/'preprint'/e['path'];b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(p)
for p in (A/'publication').iterdir():
 if p.is_file() and p.suffix in {'.py','.md','.json','.stdout','.stderr'}:add(p)
for p in P.glob('checkpoint_364_*'):
 if p.is_file() and p.suffix in {'.json','.stdout','.stderr'}:add(p)
for n in ['CURRENT_SCOPE.json','inventory.json','RESEARCH_LOG.md','checkpoint_364_preprint_publication_receipt.json','checkpoint_364_review01_publication_receipt.json','SHARED_GIT_WINDOW_STATUS.json',Path(__file__).name]:add(P/n)
allow=P/'checkpoint_364_zenodo_allowlist.json';paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_owned_paths':sorted(paths),'math_percent':100,'preprint_percent':100,'acceptance_publication_workflow_percent':95,'second_fresh_review_pending':False,'scope':'Only eligible claimed_solved PR364 accepted publication evidence and current goal bookkeeping; tracker login remains pending; private evidence excluded.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert subprocess.run(['git','merge-base','--is-ancestor',publication['actual_merge'],'HEAD'],cwd=R).returncode==0
def foreign():
 out={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1)
   if name.decode() not in paths:out.setdefault(name,[]).append(meta)
 return out
before=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish accepted biconstrained preprint DOI and exact public verification; track pending CLI login','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(args,cwd=R,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (P/('checkpoint_364_zenodo_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_364_zenodo_'+label+'.stderr')).write_bytes(r.stderr)
 (P/('checkpoint_364_zenodo_'+label+'.json')).write_text(json.dumps({'argv':args,'cwd':str(R),'started_utc':start,'finished_utc':end,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
 assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PUBLISHED_ACCEPTED_PR364_ZENODO_AND_PENDING_TRACKER_LOGIN','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True,'mathematical_resolution_percent':100,'preprint_workflow_percent':100,'acceptance_publication_workflow_percent':95,'second_review_pending':False,'merge_zenodo_pending':False,'tracker_pending':True,'doi':publication['doi'],'eligible_scope':'submitted claimed_solved exactly; skip every other status and PR8'}
(P/'checkpoint_364_zenodo_publication_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
