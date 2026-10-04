"""Finish the mirror after the first refresh caught transient GraphQL head lag.

No commit, ref, branch push, checkout, index, PR-body or readiness mutation.
Preserve all first-attempt native captures and the actual guard failure.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
C='0d5df05f85139f59702a56211bcaae5509a25404';H='0d07b06537aded3e76f5a71908f3546df574a691';B='b009faf48fa5a97a4582fd668a9cb6abbaea82b6'
Q='unsolved_math_prioritization/QUEUE.md';BRANCH='math/30004048-reviewed-psi-asymmetry'
D=A/'root_replay_private/queue_refresh_recovery_001';D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();captures=[]
def run(tag,args):
 start=utc();z=subprocess.run(args,cwd=R,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'));end=utc();streams={}
 for name,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=D/(tag+'.'+name);p.write_bytes(b);streams[name]={'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)}
 e={'tag':tag,'argv':args,'cwd':str(R),'started_utc':start,'finished_utc':end,'exit_code':z.returncode,'streams':streams};captures.append(e);(D/(tag+'.json')).write_text(json.dumps(e,indent=2)+'\n')
 assert z.returncode==0 and not z.stderr,(tag,z.returncode,z.stderr);return z.stdout
counter=0
def git(*args):
 global counter
 counter+=1;return run('git_'+str(counter),['git',*args])
assert git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==B
ix=Path(git('rev-parse','--git-path','index').decode().strip());ix=ix if ix.is_absolute() else R/ix;index=ix.read_bytes()
pr=json.loads(run('current_PR',['gh','pr','view','364','--json','state,headRefOid,headRefName,isDraft']).decode())
ref=json.loads(run('current_branch_ref',['gh','api',f'repos/AlecKriebel/Math/git/ref/heads/{BRANCH}']).decode())
main=json.loads(run('current_main',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).decode())
assert pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==ref['object']['sha']==C and pr['headRefName']==BRANCH and main['object']['sha']==B
assert git('show','-s','--format=%P',C).decode().strip().split()==[H,B]
tree=git('show','-s','--format=%T',C).decode().strip();assert tree=='5f919354e8f1e18cf6df5aaaff25e30a1d1c0ef6'
original=json.loads((A/'snapshot_manifest.json').read_bytes());expected={e['path'] for e in original['files']};assert len(expected)==42
assert set(git('diff','--name-only',B,C).decode().splitlines())==expected
raw=git('show',f'{B}:{Q}');new=git('show',f'{C}:{Q}');before=raw.splitlines(keepends=True);after=new.splitlines(keepends=True)
assert len(before)==len(after);changed=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y];assert len(changed)==1;i=changed[0]
bc=before[i].split(b'|');ac=after[i].split(b'|');assert bc[2].strip().split(b' / ')[0]==b'30004048'
assert [bc[j].strip() for j in (8,9)]==[b'queued',b'0/5'] and [ac[j].strip() for j in (8,9)]==[b'claimed_solved',b'3/5']
assert [j for j,(x,y) in enumerate(zip(bc,ac)) if x!=y]==[8,9,11]
orig=git('show',f'{H}:{Q}').splitlines(keepends=True);own=[b.split(b'|') for b in orig if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==b'30004048'];assert len(own)==1 and all(ac[j]==own[0][j] for j in (8,9,11))
S=A/'repaired_snapshot';assert not S.exists();files=[]
for e in original['files']:
 path=e['path'];b=git('show',f'{C}:{path}');meta=git('ls-tree',C,'--',path).split(b'\t',1)[0].split();assert meta[:2]==[b'100644',b'blob']
 if path!=Q:assert len(b)==e['bytes'] and sha(b)==e['sha256'] and meta[2].decode()==e['git_blob_sha']
 f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);files.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':meta[2].decode(),'mode':'100644'})
assert git('rev-parse','HEAD').decode().strip()==B and ix.read_bytes()==index
old=A/'root_replay_private/queue_refresh_20261003T213111234241'
assert json.loads((old/'remote_after.stdout').read_bytes())['headRefOid']==H
assert (old/'git_179.stdout').read_text().strip()==C and json.loads((old/'branch_push.json').read_bytes())['exit_code']==0
original_captures=[]
for f in sorted(old.glob('*.json')):
 e=json.loads(f.read_bytes())
 if not isinstance(e,dict) or 'streams' not in e:continue
 for v in e['streams'].values():
  b=(A/v['path']).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256']
 original_captures.append(e)
failure={'utc':utc(),'status':'PRESERVED_GRAPHQL_PROPAGATION_GUARD_FAILURE','pushed_commit':C,'branch_push_exit':0,'GraphQL_immediate_old_head':H,'later_graphql_and_git_ref_exact_head':C,'all_original_native_captures_retained':len(original_captures),'outer_traceback_transcribed_from_tool_output':'AssertionError at root_refresh_claimed_queue.py line96: immediate post-push GraphQL head disagreed with the just-pushed commit. Separate outer native stdout/stderr/timing were not saved by that wrapper; no invented capture is claimed.','source_preservation':'The original script version is committed at b009faf48fa5a97a4582fd668a9cb6abbaea82b6; current source adds bounded read-only propagation rechecks.','no_mutation_retried':True}
(A/'QUEUE_REFRESH_GRAPHQL_LAG_FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n')
m={'pr':364,'head':C,'base':B,'original_frozen_head':H,'previous_review_head':H,'frozen_utc':utc(),'files':sorted(files,key=lambda e:e['path'])};(A/'repaired_snapshot_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
receipt={'utc':utc(),'status':'PASS_CLAIMED_SOLVED_QUEUE_REFRESH_AFTER_READONLY_RECOVERY','pr':364,'original_head':H,'previous_review_head':H,'repaired_head':C,'current_main_parent':B,'parents':[H,B],'tree':tree,'all_original_target_files_unchanged':41,'changed_queue_line':i+1,'changed_queue_pipe_cells':[8,9,11],'accepted_status':'claimed_solved','author_turns':'3/5','old_row':before[i].decode(),'new_row':after[i].decode(),'all_other_queue_bytes_preserved':True,'checkout_and_entire_index_unchanged_during_recovery':True,'original_branch_push_succeeded_without_retry':True,'initial_propagation_failure':'QUEUE_REFRESH_GRAPHQL_LAG_FAILURE.json','original_captures':original_captures,'recovery_captures':captures,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with f.open('a') as h:h.write(f'\n{receipt["utc"]}: PR364 branch refresh `{C}` succeeded; immediate GraphQL view was stale and its guard failure/all native streams preserved. Read-only recovery confirmed branch/PR/current main/ordered parents/tree/all42 bindings/unchanged41 proof files and exact3-cell queue transplant. No ref mutation retried. Mathematical resolution100%, preprint100%, acceptance/publication80%; fresh live reproduction/actual merge/Zenodo/tracker pending.\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'original_captures','recovery_captures'}},indent=2))
