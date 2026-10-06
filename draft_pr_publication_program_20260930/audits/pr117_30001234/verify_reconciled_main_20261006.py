"""Read-only completion of fast-forward verification after self-journal guard failure."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'actual_reconciliation_verified_v3_20261006';GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'small_stdout':out.decode('utf-8','replace') if len(out)<1500 else None,'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events});require(child.returncode==0,'Read-only reconciliation check failed');return out
require(not D.exists(),'Existing verification; inspect before repeat')
D.mkdir()
window=json.loads((A/'ACTUAL_WRITER_HANDOFF_20261006.json').read_text());base=window['remote_main'];before=window['reported_sole_parent']
previous=json.loads((A/'actual_reconciliation_20261006/PROCESS_JOURNAL.json').read_text())
ff=[x for x in previous['events'] if x['argv'][1:]==['merge','--ff-only','origin/main']]
require(len(ff)==1 and ff[0]['exit_code']==0,'Actual prior fast-forward not established')
require(window['explicit_release_received'],'Actual writer release absent')
require(run(['branch','--show-current']).strip()==b'main' and run(['rev-parse','HEAD']).decode().strip()==base,'Current main mismatch')
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==base and run(['rev-parse','origin/main']).decode().strip()==base,'Current remote/fetched main mismatch')
require(run(['rev-parse',base+'^']).decode().strip()==before and run(['rev-parse',base+'^{tree}']).decode().strip()==window['reported_tree'],'Actual parent/tree mismatch')
require(not run(['diff','--name-only',before,base,'--','draft_pr_publication_program_20260930','AGENTS.md','unsolved_math_prioritization/AGENTS.md','unsolved_math_prioritization/README.md']),'Program/policy collision')
require(not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Index/materialized tracked change')
original=A/'original_head_authentication_20261006';auth=json.loads((original/'ORIGINAL_AUTHENTICATION.json').read_text())
for item in auth['original_files']:
    body=(original/'original_attempt'/item['path']).read_bytes();require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Original body changed')
family_seals=[('ideal_hypotheses_adversary_20261006','863931986a6222285d3ab840bb16b2e5054a2dabba008cc119a0f1ed9e51b9a2'),('polytope_fiber_adversary_20261006','91cfa9cfe70d53c8c238815521dbff44137873190a7e70c55a398a3dcc994f69'),('primary_source_scope_adversary_20261006','88b1428cbdd72deafe782eff2bdafaf4565c58b2adabfe68b95cd32be6ea76af'),('original_question_priority_adversary_20261006','1235924906c6fb09a18dcf1a324d06cbf42621c0c2c86758b8da0e2ce7f2d584'),('determinantal_priority_adversary_20261006','851eae3623b022dc5b33003b410cc7431ef1d2a5126e826a382c1869840b1066'),('later_binomial_priority_adversary_20261006','f7832ca2499adef7307a9d84eecc435d32693571f7f231e5116d8f21ab4fae6e'),('exact_prior_disposition_adversary_20261006','d59f9dfe58c6d00b3090cd3d325a8251d161579c81a2ba0497d228038ece64bc')]
count=0
for name,digest in family_seals:
    folder=A/name;manifest=folder/'OUTPUT_MANIFEST.json';require(sha(manifest.read_bytes())==digest,'Sealed manifest changed')
    obj=json.loads(manifest.read_text())
    for item in obj.get('members',obj.get('files',[])):
        relative=item.get('path',item.get('relative_path'));require(relative is not None,'Manifest path schema');path=Path(relative) if Path(relative).is_absolute() else folder/relative;require(path.is_relative_to(folder) and not path.is_symlink(),'Manifest namespace')
        body=path.read_bytes();require(len(body)==item.get('bytes',item.get('byte_count')) and sha(body)==item['sha256'],'Sealed family body changed');count+=1
require(count==220,'Family member total mismatch')
receipt={'schema':'pr117-read-only-reconciliation-completion/v1','UTC':now(),'actual_operator_PID':os.getpid(),'before_main':before,'remote_main':base,
 'actual_prior_fast_forward_reverified_not_repeated':True,'parent_tree_remote_main_branch_and_index_verified':True,
 'all20_original_and220_sealed_family_bodies_unchanged':True,'program_and_policy_paths_unchanged':True,'primary_checkout_mutated':False,
 'root_writer_owner':'this chat','failed_self_journal_guard_preserved':'actual_reconciliation_20261006/PROCESS_JOURNAL.json',
 'failure_reason':'The earlier public-input snapshot included its own incrementally updated journal; that mutable operational journal correctly changed. The fast-forward succeeded and no proof or audit input changed. This run authenticates immutable science members and excludes the active journal from that set.',
 'this_repair_git_ref_index_mutations':False}
dump(D/'RECEIPT.json',receipt);print(json.dumps(receipt,sort_keys=True))
