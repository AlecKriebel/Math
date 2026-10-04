"""Publish a scoped50% research checkpoint; preprint reviews and acceptance pending."""
from pathlib import Path
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr356_30001552'
PREFIX='checkpoint_356_priority_preprint'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def window():assert not json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
assert not (P/(PREFIX+'_receipt.json')).exists() and not (P/(PREFIX+'_stage.json')).exists()
assert json.loads((A/'ROOT_PRIORITY_POSTCLOSURE_REPLAY.json').read_bytes())['status']=='PASS_EXACT_PRIORITY_NATIVE_REPLAY_POSTCLOSURE'
assert json.loads((A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json').read_bytes())['status']=='PASS_EXACT_PDF_SOURCE_METADATA_AND_WHOLE_PUBLIC_PACKAGE'
c=json.loads((A/'acceptance_criteria.json').read_bytes());assert not c['candidate_accepted'] and c['acceptance_publication_workflow_percent']==50
paths=set()
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 paths.add(str(p.relative_to(R)))
for name in ['.gitignore','README.md','RESEARCH_LOG.md','acceptance_criteria.json','PREPRINT_PLAN.md',
 'root_replay_priority.py','ROOT_PRIORITY_PRECLOSURE_REPLAY.json','ROOT_PRIORITY_POSTCLOSURE_REPLAY.json',
 'root_verify_preprint.py','ROOT_PREPRINT_PACKAGE_VERIFICATION.json','PREPRINT_EXPORT_SEQUENCE_REPAIR.json',
 'ROOT_PREPRINT01_SOURCE_GATE.json','root_refresh_claimed_queue.py']:add(A/name)
for name in ['alternating-antimorphic-fine-wilf.tex','alternating-antimorphic-fine-wilf.pdf',
 'alternating-antimorphic-verification.zip','zenodo-deposit.json','verify_supplement.py','build_supplement.py','PACKAGE_BUILD.json']:add(A/'preprint'/name)
priority=A/'priority_review';manifest=json.loads((priority/'PUBLIC_MANIFEST.json').read_bytes())
for name in manifest['inventory_paths']+['CLOSURE.json']:
 assert Path(name).name==name;add(priority/name)
for name in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_356_closed_math_receipt.json',
 'root_dedup_root_captures_20261004.py','ROOT_CAPTURE_DEDUP_20261004T0140.json','ROOT_CAPTURE_DEDUP_20261004T0140.jsonl',Path(__file__).name]:add(P/name)
allow=P/(PREFIX+'_allowlist.json');paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'math_completion_percent':100,'bounded_priority_percent':100,'workflow_percent':50,
 'scope':'Closed curated priority audit, reproduced draft preprint and root receipts. New final preprint adversaries pending; no promotion/merge/deposit/tracker; no raw sources/private native capture files.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
assert git('branch','--show-current')==b'main\n' and not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
 result={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1)
   if name.decode() not in paths:result.setdefault(name,[]).append(meta)
 return result
before=foreign();parent=git('rev-parse','HEAD').decode().strip();assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),
 ('commit',['git','commit','--only','-m','Complete bounded antimorphic priority audit and draft reproduced research note','--',*sorted(paths)]),
 ('push',['git','push','origin','main'])]:
 window();started=utc();(P/(PREFIX+'_'+label+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 r=subprocess.run(args,cwd=R,capture_output=True)
 for kind,b in [('stdout',r.stdout),('stderr',r.stderr)]: (P/(PREFIX+'_'+label+'.'+kind)).write_bytes(b)
 (P/(PREFIX+'_'+label+'.json')).write_text(json.dumps({'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':r.returncode,
 'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)},indent=2)+'\n')
 assert r.returncode==0,(label,r.stderr.decode(errors='replace'));assert foreign()==before
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit
for path in paths:assert git('show',commit+':'+path)==(R/path).read_bytes(),path
r={'utc':utc(),'status':'PASS_PR356_PRIORITY_AND_DRAFT_CHECKPOINT_PUSHED_FULL_READBACK','commit':commit,'parent':parent,
 'changed_owned_paths':len(changed),'allowlist_paths':len(paths),'all_allowlisted_git_disk_bytes_equal':True,'remote_main_exact':True,
 'foreign_staged_entries_preserved':True,'mathematical_audit_percent':100,'bounded_priority_percent':100,'workflow_percent':50,
 'fresh_preprint_reviews_pending':True,'promoted':False}
(P/(PREFIX+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
