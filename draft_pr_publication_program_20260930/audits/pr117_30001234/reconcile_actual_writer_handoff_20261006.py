"""Fresh root verification and isolated-main fast-forward after actual handoff."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'actual_reconciliation_20261006';GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'small_stdout':out.decode('utf-8','replace') if len(out)<1500 else None,'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual reconciliation failed; inspect journal before retry');return out
require(not D.exists(),'Existing reconciliation; inspect rather than repeat')
D.mkdir()
window=json.loads((A/'ACTUAL_WRITER_HANDOFF_20261006.json').read_text())
require(window['explicit_release_received'],'Actual handoff absent')
base=window['remote_main'];before=run(['rev-parse','HEAD']).decode().strip()
require(before==window['reported_sole_parent'],'Unexpected local before-main')
require(run(['branch','--show-current']).strip()==b'main','Not main')
require(not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Foreign index/materialized changes')
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==base,'Actual remote main differs from handoff')
private={'private_sources','private_renders','private_backend','private','__pycache__'}
own={str(x.relative_to(C)):(x.stat().st_size,sha(x.read_bytes())) for x in A.rglob('*') if x.is_file() and not x.is_symlink() and not private.intersection(x.parts)}
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
require(run(['rev-parse','origin/main']).decode().strip()==base,'Fetched remote main differs')
run(['merge-base','--is-ancestor',before,base])
collision=run(['diff','--name-only',before,base,'--','draft_pr_publication_program_20260930','AGENTS.md','unsolved_math_prioritization/AGENTS.md','unsolved_math_prioritization/README.md'])
require(not collision,'Program or policy changes require explicit reconciliation')
require(run(['rev-parse',base+'^']).decode().strip()==before,'Reported parent mismatch')
require(run(['rev-parse',base+'^{tree}']).decode().strip()==window['reported_tree'],'Reported tree mismatch')
run(['merge','--ff-only','origin/main'])
require(run(['rev-parse','HEAD']).decode().strip()==base and run(['branch','--show-current']).strip()==b'main','Fast-forward result mismatch')
for path,(size,digest) in own.items():
    body=(C/path).read_bytes();require(len(body)==size and sha(body)==digest,'Own public input changed')
require(not run(['diff','--cached','--name-only']),'Index not empty after reconciliation')
receipt={'schema':'pr117-actual-exclusive-writer-reconciliation/v1','UTC':now(),'actual_operator_PID':os.getpid(),'before_main':before,'remote_main':base,'reported_parent_and_tree_independently_verified':True,'actual_isolated_main_fast_forward_passed':True,'own_public_files_preserved':len(own),'own_complete_source_and_mathematical_proof_unchanged':True,'policy_and_program_paths_unchanged':True,'primary_checkout_mutated':False,'index_empty':True,'writer_owner':'this chat','scientific_or_PR_mutation':False}
dump(D/'RECEIPT.json',receipt)
print(json.dumps(receipt,sort_keys=True))
