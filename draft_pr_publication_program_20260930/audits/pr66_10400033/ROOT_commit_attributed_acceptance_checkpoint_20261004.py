"""Scoped public audit checkpoint after actual attributed acceptance readback."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess, sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no optimization')
A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
PREP = A / 'attributed_integration_preparation_20261004'
F = A / 'ROOT_attributed_acceptance_checkpoint_20261004'
F.mkdir(exist_ok=False)
D = F / 'private_actual_git_commands'
D.mkdir()
(D / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
records = []
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_bytes())
def require(c, msg):
    if not c: raise RuntimeError(msg)
def names(b): return {x.decode() for x in b.split(b'\0') if x}
def pin(n):
    p = R / n
    if not p.exists(): return {'absent':True}
    require(p.is_file() and not p.is_symlink(), 'Unexpected path type: '+n)
    b = p.read_bytes()
    return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def run(*args):
    argv=['git','--no-optional-locks',*args]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate();n=str(len(records)+1)
    (D/(n+'.stdout')).write_bytes(out);(D/(n+'.stderr')).write_bytes(err)
    records.append({'argv':argv,'actual_pid':child.pid,'cwd':str(R),'start_utc':start,
                    'finish_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,
                    'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    (D/'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n')
    require(child.returncode==0,'Git failure; inspect preserved streams')
    return out

gate=read(A/'ROOT_FINAL_PRIOR_DISPOSITION_20261004.json')
ackpath=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
ackbytes=ackpath.read_bytes()
def window():
    w=read(ackpath)
    require(ackpath.read_bytes()==ackbytes and w['shared_git_writes_paused'] is True
            and w['paused_for']=='PR66 attributed prior-result integration 20261004'
            and w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True
            and w['all_staged_path_count']==0 and w['owned_staged_paths']==[]
            and w['local_main_at_pause']==w['remote_main_at_pause']
            and dt.datetime.fromisoformat(w['utc'])>=dt.datetime.fromisoformat(gate['minimum_writer_ack_utc']),
            'Fresh writer freeze absent or changed')
    return w
w=window()
require(run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z'),'Branch/index drift')
base=run('rev-parse','HEAD').decode().strip()
merge=read(PREP/'native_attributed_result_operations_20261004/NATIVE_MERGE_RESULT.json')
accept=read(PREP/'native_attributed_result_operations_20261004/NATIVE_ACCEPTANCE_RESULT.json')
require(base==accept['acceptance_commit']==run('ls-remote','--heads','origin','main').decode().split()[0]
        and merge['base']==w['local_main_at_pause'],'Native chain/main/remote drift')
readback=read(PREP/'ROOT_attributed_acceptance_readback_20261004/ACCEPTANCE_READBACK.json')
require(readback['status']=='PASS' and readback['native_acceptance_verified'] is True
        and readback['current_commit']==base and readback['GitHub_accepted_metadata_verified'] is True,'Acceptance readback absent')
progress=read(P/'CURRENT_PROGRESS.json')
require(progress['current_PR']==66 and progress['current_PR_workflow_percent']==95
        and progress['current_audited_outcome']=='already_solved'
        and not progress['current_publication_authorization'] and not progress['current_priority_clearance']
        and not progress['persistent_goal_complete'],'Ready progress differs')
rootfiles=['RESEARCH_LOG.md','ROOT_FINAL_PRIOR_DISPOSITION_20261004.json',
           'ROOT_finalize_prior_disposition_20261004.py',
           'ROOT_verify_completed_priority_families_20261004.py','ROOT_prepare_attribution_v2_20261004.py',
           'ROOT_commit_attributed_acceptance_checkpoint_20261004.py']
roots=[A/x for x in rootfiles]+[P/'CURRENT_PROGRESS.json']
folders=['ROOT_priority_audit_20261004','ROOT_completed_priority_family_readback_20261004',
         'mathematical_checkpoint_20261004',
         'exact_target_priority_20261004','mechanism_priority_20261004',
         'prior_disposition_fresh_adversary_20261004',
         'attributed_prior_result_preparation_20261004','attributed_prior_result_preparation_v2_20261004',
         'attributed_integration_preparation_20261004','ROOT_fresh_disposition_custody_readback_20261004']
blockedparts={'private_actual_git_commands','preparation_command_streams','primary_sources','__pycache__','raw','pixels'}
allowed={'.md','.json','.jsonl','.py','.sha256'}
for n in folders:
    for f in (A/n).rglob('*'):
        if f.is_file() and f.suffix in allowed and not any(x in blockedparts for x in f.parts): roots.append(f)
# Include metadata and recorder source for actual ROOT captures, never source/Git stream bodies.
C=P/'audits/pr45_9900007'
captures=['root_pr66_priority_Fiedler_Stoimenow_author_retrieval_20261004_actual_capture',
          'root_pr66_priority_Fiedler_Stoimenow_extract_20261004_actual_capture',
          'root_pr66_priority_Fiedler_Stoimenow_scope_pixels_20261004_actual_capture',
          'root_pr66_completed_priority_custody_20261004_actual_capture',
          'root_pr66_attribution_v2_preparation_20261004_actual_capture',
          'root_pr66_fresh_disposition_custody_20261004_actual_capture',
          'root_pr66_attributed_native_merge_20261004_actual_capture',
          'root_pr66_attributed_merge_readback_20261004_actual_capture',
          'root_pr66_attributed_native_mirror_20261004_actual_capture',
          'root_pr66_attributed_PR_metadata_correction_20261004_actual_capture',
          'root_pr66_attributed_acceptance_readback_20261004_actual_capture']
for n in captures:
    require(read(C/n/'CAPTURE.json')['status']=='PASS','Actual ROOT capture incomplete: '+n)
    roots.extend([C/n/'CAPTURE.json',C/n/'prelaunch_operator.py'])
rel=sorted(set(str(x.relative_to(R)) for x in roots))
require(all((R/x).is_file() and not (R/x).is_symlink() for x in rel),'Owned selection missing/nonregular')
selected=names(run('diff','--name-only','-z','--',*rel))|names(run('ls-files','--others','--exclude-standard','-z','--',*rel))
require(selected and selected<=set(rel),'Selection scope differs')
require(all(Path(x).suffix in allowed and not any(t in blockedparts for t in Path(x).parts) for x in selected),'Private/copyright body included')
owned={x:pin(x) for x in sorted(selected)}
foreign={x:pin(x) for x in names(run('diff','--name-only','-z'))-selected}
native={x:pin(x) for x in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']}
plan={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),
      'base':base,'acknowledgement_sha256':sha(ackbytes),'owned':owned,'foreign':foreign,
      'native_to_preserve':native,'native_acceptance_independently_read_back':True,
      'copyright_sources_and_all_stream_bodies_excluded':True,
      'full_local_manifests_do_not_assert_Git_inclusion':True,'new_paper':False,'new_DOI':None}
planpath=F/'PLAN.json';planpath.write_text(json.dumps(plan,indent=2)+'\n')
planname=str(planpath.relative_to(R));selected.add(planname);owned[planname]=pin(planname)
def preserve():
    window()
    require(names(run('diff','--name-only','-z'))-selected==set(foreign),'Foreign tracked scope drift')
    for n,r in {**foreign,**owned,**native}.items():require(pin(n)==r,'Whole body/mode drift: '+n)
preserve();run('add','--',*sorted(selected))
require(names(run('diff','--cached','--name-only','-z'))==selected,'Staged scope differs')
for n,r in owned.items():require(sha(run('show',':'+n))==r['sha256'],'Index bytes differ: '+n)
preserve();run('commit','-m','Record PR66 prior-bound attribution and independently verified acceptance')
commit=run('rev-parse','HEAD').decode().strip()
require(run('show','-s','--format=%P',commit).decode().strip()==base
        and names(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected,'Commit parent/scope differs')
require(run('ls-remote','--heads','origin','main').decode().split()[0]==base,'Remote advanced before push')
preserve();run('push','origin','main')
require(run('ls-remote','--heads','origin','main').decode().split()[0]==commit
        and not run('diff','--cached','--name-only','-z'),'Push/index readback failure')
preserve()
receipt={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),
         'status':'PASS','commit':commit,'base':base,'remote_main':commit,'owned_path_count':len(selected),
         'foreign_tracked_paths_preserved':len(foreign),'index_empty':True,'native_QUEUE_state_history_unchanged':True,
         'current_PR_workflow_percent':100,'merge_commit':merge['merge_commit'],
         'acceptance_commit':accept['acceptance_commit'],'audited_outcome':'already_solved',
         'accepted_as':'attributed_partial_prior_result','new_paper':False,'new_DOI':None,'goal_complete':False,
         'receipt_created_after_push_not_in_own_commit':True}
(F/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
