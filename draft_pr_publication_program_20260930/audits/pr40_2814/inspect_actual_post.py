"""ROOT whole actual post inspection; no acceptance helper import/execution."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import subprocess

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr40_2814'
K=R/'unsolved_math_prioritization/attempts/2814'
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):
    def pairs(items):
        o={}
        for k,v in items:
            assert k not in o
            o[k]=v
        return o
    return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def check(p,z):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    b=p.read_bytes();size=z.get('bytes',z.get('size'))
    assert type(size) is int and len(b)==size and H(b)==z['sha256'],str(p)
    return b
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def closure(p,pin,count,mode=None):
    assert H(p.read_bytes())==pin
    m=J(p);names=set()
    for z in m['files']:
        n=z['path'];assert n not in names and not n.startswith('/') and not set(n.split('/'))&{'','.','..'}
        names.add(n);check(p.parent/n,z)
        if mode is not None:assert stat.S_IMODE((p.parent/n).stat().st_mode)==mode
    assert len(names)==count
    assert {f.relative_to(p.parent).as_posix() for f in p.parent.rglob('*') if f.is_file()}==names|{p.name}
    if mode is not None:assert stat.S_IMODE(p.stat().st_mode)==mode
    return m

C=A/'root_integration_post_actual_capture';cap=J(C/'CAPTURE.json')
assert cap['actual_execution'] is True and cap['completed'] is True and cap['status']=='PASS'
assert type(cap['pid']) is int and cap['pid']==1567 and cap['exit_code']==0 and cap['outer_errors']==[]
assert cap['head_before']==cap['head_after']=='c44e1c83bd4aecc588bbc58ea14207e1275c7dd7'
assert git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==cap['head_after']
assert cap['fresh_native13_before']==cap['fresh_native13_after'] and cap['fresh_native13_modes_before']==cap['fresh_native13_modes_after']
assert cap['actual_changed_native_inputs']==cap['actual_changed_native_modes']==cap['allowed_changed_native_inputs']==cap['allowed_changed_native_modes']==[]
assert len(cap['fresh_native13_after'])==13
for z in cap['fresh_native13_after']:
    check(R/z['path'],z);assert stat.S_IMODE((R/z['path']).stat().st_mode)==cap['fresh_native13_modes_after'][z['path']]
for z in cap['complete_root_review_pins'].values():assert type(z['bytes']) is int
for n,z in cap['complete_root_review_pins'].items():
    check(R/n,z);assert stat.S_IMODE((R/n).stat().st_mode)==z['mode']
for f in ('stdout','stderr'):check(C/cap[f]['path'],cap[f])
assert not (C/cap['stderr']['path']).read_bytes()
assert J(C/cap['stdout']['path'])==dict(new_proof_turns=0,pr=40,primary_acceptances=30,status='PASS',targets=31,turns=37)
source=Path(cap['argv'][2]);assert H(source.read_bytes())==cap['source_sha256'] and stat.S_IMODE(source.stat().st_mode)==cap['source_mode']
assert H((source.parent/'pr40_guards.py').read_bytes())==cap['guards_sha256']
start=dt.datetime.fromisoformat(cap['started_utc']);finish=dt.datetime.fromisoformat(cap['finished_utc'])
assert start.tzinfo is not None and finish.tzinfo is not None and start<=finish<=dt.datetime.now(dt.timezone.utc)
post=J(A/'post_acceptance_verification.json')
assert start<=dt.datetime.fromisoformat(post['utc'])<=finish
for key,value in dict(status='PASS',pr=40,actual_remote_state='MERGED',targets=31,consumed_substantive_turns=37,primary_acceptances=30,program_completed_count=30,new_proof_turns=0,workflow_completion_estimate_percent=100,scientific_completion_estimate_percent=0).items():
    assert type(post[key]) is type(value) and post[key]==value
assert type(post['program_completion_estimate_percent']) is float and post['program_completion_estimate_percent']==30/180*100
for k in ['full_problem_solved','novelty_claimed','paper_or_new_doi_or_tracker','duplicate_native_acceptance_added']:assert post[k] is False
for k in ['fresh_native_mirror_noop','current_metadata_present_null','entire_history_prefix_and30prior_states_preserved','one_present_primary_event','exact_original13_and_SOURCE_STATUS_unchanged','whole_current_and216dependencies_bound']:assert post[k] is True
accepted=J(A/'acceptance.json');canonical=J(K/'acceptance.json')
assert canonical=={k:v for k,v in accepted.items() if k not in {'canonical_manifest_sha256','canonical_manifest_entries'}}
assert accepted['partial_valid'] is True and accepted['full_problem_solved'] is accepted['novelty_claimed'] is accepted['paper_or_new_doi_or_tracker'] is False
for k in ['original_substantive_attempts','new_substantive_attempts','audit_turns','substantive_attempts_used']:assert type(accepted[k]) is int and accepted[k]==0
assert accepted['substantive_attempt_limit']==accepted['turn_limit']==5
for k in ['current_model','current_reasoning_effort','current_deadline_utc']:assert k in accepted and accepted[k] is None
canonical_manifest=closure(K/'MANIFEST.json',accepted['canonical_manifest_sha256'],247,0o444)
assert accepted['canonical_manifest_entries']==247
current_manifest=closure(A/'reviewed_candidate/MANIFEST.json','8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f',239,0o444)
deps=J(A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')
assert H((A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_bytes())=='b2c6d31f3e7230e132761322bef9d3b99e1b0f53521fbefc5a281e6682199a37' and len(deps['files'])==216
for z in deps['files']:check(A/z['path'],z)
snapshot=J(A/'snapshot_manifest.json');assert len(snapshot['files'])==13
for z in snapshot['files']:check(K/'original_archive'/z['path'],z)
assert H((K/'SOURCE_STATUS.md').read_bytes())=='c232697fb80c20a88efe7db12390d9bda2d7f5c2fdc96e5cfad3a98a8cfdf16c'
assert H((K/'turns.json').read_bytes())=='3d74f9a6f0185e200349b2f303468d1c97fd7379dd470ea12dfca22585745a62'
remote=J(A/'remote_merge_receipt.json');assert remote['number']==40 and remote['state']=='MERGED' and remote['isDraft'] is False
assert remote['headRefOid']=='163e34d566d6cbaee3a2a8fdc6394fbb9e49a539' and remote['mergeCommit']['oid']==post['merge_commit']==cap['head_after']
assert git('show','-s','--format=%P',post['merge_commit']).decode().strip().split()==['f56477f54beb48eae1dc828da06eb195d07a0b3a',remote['headRefOid']]
assert git('show','-s','--format=%T',post['merge_commit']).decode().strip()==post['merge_tree']=='024e1cf109fbb1416828e4800eab0693055a3a78'
intent=J(A/'state_mirror_intent.json');old=json.loads(intent['before_state_bytes']);state=J(R/'unsolved_math_prioritization/state.json')
assert len(old)==30 and len(state)==31 and set(state)-set(old)=={'2814'} and all(state[k]==v for k,v in old.items())
history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();prefix=intent['before_history_bytes'].encode()
assert history.startswith(prefix);events=[json.loads(x) for x in history[len(prefix):].splitlines()]
assert len(events)==1 and events[0]['id']=='2814' and events[0]['turns_used']==0 and events[0]['pr']==40
assert '20001896' not in state and sum(z['turns_used'] for z in state.values())==37
mirror=J(A/'state_mirror_receipt.json');assert H(history)==mirror['history_sha256'] and H((R/'unsolved_math_prioritization/state.json').read_bytes())==mirror['state_sha256']
pre=J(A/'integration_preflight.json')
for z in pre['foreign_logs']:check(R/z['path'],z)
receipt=dict(schema='pr40-root-entire-actual-post-inspection/v1',status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_post_pid=cap['pid'],capture_sha256=H((C/'CAPTURE.json').read_bytes()),complete_post_object=post,entire_capture_object=cap,complete_remote_object=remote,complete_mirror_receipt=mirror,whole_canonical_members=247,current_members=239,individual_dependencies=216,all_native13_bytes_modes_unchanged=True,full_prior30_states_and_history_prefix_preserved=True,full_problem_solved=False,new_substantive_attempts=0,audit_turns=0,completed_primary_prs=30,total_primary_prs=180,completion_percent=30/180*100)
with (A/'ROOT_ACTUAL_POST_INSPECTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',actual_post_pid=cap['pid'],canonical_members=247,completed_primary_prs=30,completion_percent=30/180*100)))
