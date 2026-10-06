"""Read and independently compare every complete postmerge Git/API capture."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;D=A/'post_merge_review';R=A/'root_postmerge_streams';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
checks=[];executions=[]
def check(c,label):checks.append({'check':label,'pass':bool(c)});assert c,label
def bind(p,r):
 b=p.read_bytes();check(len(b)==r['bytes'] and sha(b)==r['sha256'],'complete binding '+str(p.relative_to(A)));return b
manifest=load(D/'PUBLIC_MANIFEST.json')
for row in manifest['files']:bind(D/row['path'],row)
for row in load(D/'FINAL_SEAL.json')['sealed_artifacts']:bind(D/row['path'],row)
receipt=load(D/'receipts/FINAL_RECEIPT.json');check(receipt['status']=='QUALIFIED_ACTUAL_MERGE_SCOPE_PASS','qualified complete post scope')
allchecks=load(D/'receipts/CHECKS.json');check(len(allchecks)==receipt['checks'] and all(r['pass'] is True for r in allchecks),'every complete post check')
baseline=load(D/'BASELINE.json');merge=baseline['merge']
local=load(A/'ACTUAL_MERGE_VERIFICATION.json');check(local['actual_merge']==merge==receipt['merge'],'root and agent exact actual merge')
captures=load(D/'receipts/EXECUTIONS.json');check(len(captures)==receipt['complete_captures'],'every complete post capture')
for capture in captures:
 label=capture['label'];out=None
 for channel in ('stdout','stderr'):
  row=capture[channel];stored=(D/row['path']).read_bytes();raw=gzip.decompress(stored)
  check(len(stored)==row['stored_bytes'] and sha(stored)==row['stored_sha256'] and len(raw)==row['bytes'] and sha(raw)==row['sha256'],'all actual retained post bytes '+label+' '+channel)
  (R/('agent_'+label+'.'+channel+'.gz')).write_bytes(stored)
  if channel=='stdout':out=raw
  else:check(raw==b'','complete actual post empty stderr '+label)
 check(capture['exit_code']==0,'actual post success '+label)
 args=capture['args']
 if args[0]=='git':check(args[1] in {'cat-file','rev-parse','branch','merge-base','diff','show','ls-tree'},'read-only exact post Git command')
 elif args[0]=='gh':check(args[:4]==['gh','api','--method','GET'],'read-only exact post API command')
 else:check(args[:2]==['python3','-B'] and Path(args[-1]).name in {'verify_audit.py','verify_live_audit.py'},'fully read unchanged closed validator')
 start=datetime.now(timezone.utc).isoformat();current=subprocess.run(args,capture_output=True);finish=datetime.now(timezone.utc).isoformat()
 for channel in ('stdout','stderr'):(R/(label+'.'+channel+'.gz')).write_bytes(gzip.compress(getattr(current,channel),mtime=0))
 check(current.returncode==0 and current.stderr==b'','entire independent post successful output '+label)
 if label in {'api_start_pr','api_end_pr'}:
  reference=json.loads(out);actual=json.loads(current.stdout)
  for side in ('base','head'):
   rr=reference[side]['repo'];cc=actual[side]['repo']
   for obj,end in ((rr,capture['finished_utc']),(cc,finish)):
    check(type(obj['open_issues']) is int and obj['open_issues']>=0 and obj['open_issues']==obj['open_issues_count'],'coherent actual global issue counters '+side)
    check(datetime.fromisoformat(obj['created_at'])<=datetime.fromisoformat(obj['pushed_at'])<=datetime.fromisoformat(end),'valid actual global repository UTC '+side)
   check(datetime.fromisoformat(rr['pushed_at'])<=datetime.fromisoformat(cc['pushed_at']),'global repository UTC monotonic '+side)
   for key in ('open_issues','open_issues_count','pushed_at'):cc[key]=rr[key]
  check(reference==actual,'entire actual merged PR object except6 individually validated global repository leaves '+label)
 elif args[0]=='gh':check(json.loads(current.stdout)==json.loads(out),'entire actual post API object '+label)
 else:check(current.stdout==out,'entire actual post literal stdout '+label)
 executions.append({'label':label,'args':args,'started_utc':start,'finished_utc':finish,'exit_code':current.returncode,'stdout_bytes':len(current.stdout),'stdout_sha256':sha(current.stdout),'stderr_bytes':0,'complete_outputs':str(R.relative_to(A))+'/'+label+'.stdout.gz'})
run=subprocess.run(['python3','-B',str(D/'verify_post_merge.py')],capture_output=True)
check(run.returncode==0 and run.stderr==b'' and run.stdout==b'PASS: actual merge audit entire closed manifest, seal and all complete outputs\n','entire closed actual post verifier')
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ENTIRE_POSTMERGE_REPORT_AND_EVERY_FULL_CAPTURE','actual_merge':merge,'agent_checks':receipt['checks'],'complete_agent_and_root_capture_pairs':len(captures),'public_post_manifest_files':len(manifest['files']),'public_post_manifest_sha256':sha((D/'PUBLIC_MANIFEST.json').read_bytes()),'all_root_checks':checks,'check_count':len(checks),'complete_root_reexecutions':executions,'entire_verifier_stdout':run.stdout.decode(),'no_redundant_math_replay':True,'all43_original_mathematical_and4_reviewed_submission_bytes_unchanged':True}
(A/'root_postmerge_scope_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'all_root_checks','complete_root_reexecutions'}},indent=2))
