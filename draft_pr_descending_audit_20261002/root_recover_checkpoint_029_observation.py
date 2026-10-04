"""Read back a successful scoped push after the final foreign-observation guard failed."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, subprocess, stat, os

P = Path(__file__).resolve().parent
R = P.parent
A = P/'audits/pr311_30005303'
D = P/'private_checkpoint_311_publication_preparation_029'
OUT = P/'private_checkpoint_311_publication_preparation_029_readback'
OUT.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
load = lambda p: json.loads(p.read_bytes())
records = []

def git(*args):
    label = 'git_'+str(len(records))
    start = utc()
    r = subprocess.run(['/usr/bin/git',*args],cwd=R,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    rec = {'argv':['/usr/bin/git',*args],'started_utc':start,'ended_utc':utc(),'exit_code':r.returncode}
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (OUT/(label+'.'+k)).write_bytes(b)
        rec[k+'_bytes'] = len(b)
        rec[k+'_sha256'] = sha(b)
    (OUT/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    records.append(rec)
    assert r.returncode == 0
    return r.stdout

allowed = set(load(P/'checkpoint_311_publication_preparation_029_allowlist.json')['paths'])
head = '29c5723c30d78825938e3782676d3e2bbe16a6bb'
parent = '3d577b9c99c83aeae38f933f423dac3332dce5cc'
assert git('branch','--show-current') == b'main\n'
assert git('rev-parse','HEAD').decode().strip() == head
assert git('show','-s','--format=%P',head).decode().strip() == parent
assert git('ls-remote','origin','refs/heads/main').decode().split()[0] == head
assert not git('diff','--cached','--raw','-z')
changed = set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
assert changed == allowed and len(changed) == 20
assert all(git('show',head+':'+p) == (R/p).read_bytes() for p in allowed)
# Both stage and commit passed the exact foreign index/body/mode guard.
# The push exited zero, then that observation guard failed. The old body
# inventory existed only in the terminated process's memory: do not pretend
# that the exact changed foreign body can now be reconstructed from it.
for phase in ['stage','commit','push']:
    r = load(D/(phase+'_execution.json'))
    assert r['exit_code'] == 0
    for stream in ['stdout','stderr']:
        assert sha((D/(phase+'.'+stream)).read_bytes()) == r[stream+'_sha256']
dirty = {}
for n in git('diff','--name-only','-z').split(b'\0'):
    if n and n.decode() not in allowed:
        p = R/n.decode()
        dirty[n.decode()] = {'exists':p.exists(),'bytes':p.stat().st_size if p.is_file() else None,
                            'sha256':sha(p.read_bytes()) if p.is_file() else None,
                            'mode':format(stat.S_IMODE(p.stat().st_mode),'04o') if p.exists() else None,
                            'mtime_ns':p.stat().st_mtime_ns if p.exists() else None}
(OUT/'CURRENT_FOREIGN_TRACKED_OBSERVATION.json').write_text(json.dumps({'recorded_utc':utc(),'files':dirty},indent=2)+'\n')
result = {'utc':utc(),'status':'PASS_SCOPED_CHECKPOINT_REMOTE_READBACK_WITH_FOREIGN_OBSERVATION_GUARD_FAILURE',
    'parent':parent,'commit':head,'changed_paths':20,'allowlist_paths':20,'entire_index_empty':True,'remote_main_exact':True,
    'all_twenty_committed_bodies_exact':True,'foreign_committed_tree_and_index_unchanged':True,
    'foreign_body_mode_guard_passed_through_stage_and_commit':True,
    'foreign_body_mode_guard_passed_after_push':False,'foreign_body_inventory_before_push_not_persisted':True,
    'specific_changed_foreign_body_not_retrospectively_certified':True,
    'no_foreign_write_reset_restore_or_stage_initiated':True,'automatic_commit_or_push_retry':False,
    'all_three_native_git_commands_exit_zero':True,'outer_native_operator_exit_code':1,
    'original_failure_capture':'audits/pr311_30005303/root_runs_private/pr311_publication_preparation_checkpoint029_actual001',
    'readback_capture_directory':str(OUT),'math_percent':100,'bounded_priority_percent':100,'workflow_percent':65,
    'publication_ready':False,'goal_complete':False}
with (P/'checkpoint_311_publication_preparation_029_receipt.json').open('x') as f:
    f.write(json.dumps(result,indent=2)+'\n')
s = load(P/'SHARED_GIT_WINDOW_STATUS.json')
assert not s['shared_git_writes_paused']
s.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,
         last_owned_checkpoint_pushed=True,descending_checkpoint_029_foreign_observation_guard_failure_retained=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:
        f.write('\n'+utc()+' — CP029 actual stage/commit/push each exited0 and main/remote are29c5723c30d78825938e3782676d3e2bbe16a6bb. The outer operator then exited1 because its foreign body/mode observation changed after the successful push; exact guard passed through stage and commit. Independent readback verifies exact20allowlisted committed paths and bodies, unchanged foreign committed tree/index, empty entire index and current remote. The old foreign body inventory was memory-only, so the specific concurrent change and full post-push body equality are not retrospectively certified. No foreign files were written, restored, reset or staged; no mutation was retried. Failure preserved, current foreign observation saved privately; future checkpoint guards must persist their before inventory. Math100%,boundedpriority100%,workflow65%; NEWfullreview02 still active and no publication clearance.\n')
print(json.dumps(result,indent=2))
